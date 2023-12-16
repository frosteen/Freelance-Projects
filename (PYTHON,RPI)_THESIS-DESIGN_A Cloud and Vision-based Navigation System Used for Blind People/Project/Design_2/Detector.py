import cv2
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer, _PanopticPrediction, GenericMask
import pycocotools.mask as mask_util


def centroid(vertexes):
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return (_x, _y)


class Detector:
    def __init__(self, model_type="OD", threshold=0.5, use_gpu=False):
        self.cfg = get_cfg()
        self.model_type = model_type

        # Load model config and pretrained model
        if model_type == "OD":  # object detection
            yaml_file = "COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"
            self.cfg.merge_from_file(model_zoo.get_config_file(yaml_file))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(yaml_file)

        elif model_type == "IS":  # instance segmentation
            yaml_file = "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
            self.cfg.merge_from_file(model_zoo.get_config_file(yaml_file))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(yaml_file)

        elif model_type == "KP":  # keypoint detection
            yaml_file = "COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x.yaml"
            self.cfg.merge_from_file(model_zoo.get_config_file(yaml_file))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(yaml_file)

        elif model_type == "LVIS":  # LVIS segmentation
            yaml_file = (
                "LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"
            )
            self.cfg.merge_from_file(model_zoo.get_config_file(yaml_file))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(yaml_file)

        elif model_type == "PS":  # panoptic segmentation
            yaml_file = "COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"
            self.cfg.merge_from_file(model_zoo.get_config_file(yaml_file))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(yaml_file)

        # set threshold for this model
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold

        # gpu or cpu
        if use_gpu:
            self.cfg.MODEL.DEVICE = "cuda"
        else:
            self.cfg.MODEL.DEVICE = "cpu"

        self.predictor = DefaultPredictor(self.cfg)

    def on_image(self, image):
        if self.model_type != "PS":
            predictions = self.predictor(image)["instances"]
            viz = Visualizer(
                image[:, :, ::-1],
                metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
            )
            output = viz.draw_instance_predictions(predictions.to("cpu"))

            pred_classes = predictions.pred_classes.cpu().tolist()
            pred_boxes = predictions.pred_boxes.tensor.cpu().tolist()
            class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
            pred_class_names = list(map(lambda x: class_names[x], pred_classes))
            class_names_center = []

            for class_name, box in zip(pred_class_names, pred_boxes):
                class_names_center.append(
                    {
                        "class_name": class_name,
                        "center": (
                            int((box[0] + box[2]) / 2),
                            int((box[1] + box[3]) / 2),
                        ),
                    }
                )

            return output.get_image()[:, :, ::-1], class_names_center
        else:
            predictions, segment_info = self.predictor(image)["panoptic_seg"]
            viz = Visualizer(
                image[:, :, ::-1],
                metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
            )
            output = viz.draw_panoptic_seg_predictions(
                predictions.to("cpu"), segment_info
            )

            # pred = _PanopticPrediction(
            #     predictions.to("cpu"),
            #     segment_info,
            #     MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
            # )
            # for mask, sinfo in pred.semantic_masks():
            #     binary_mask = mask.astype("uint8")  # opencv needs uint8
            #     mask = GenericMask(binary_mask, output.height, output.width)
            #     shape2d = (binary_mask.shape[0], binary_mask.shape[1])
            #     area_threshold = 10
            #     # draw polygons for regular masks
            #     for segment in mask.polygons:
            #         area = mask_util.area(
            #             mask_util.frPyObjects([segment], shape2d[0], shape2d[1])
            #         )
            #         if area < (area_threshold or 0):
            #             continue
            #         has_valid_segment = True
            #         segment = segment.reshape(-1, 2)

            #         calc_centroid = centroid(segment)
            #         cv2.circle(
            #             image,
            #             (int(calc_centroid[0]), int(calc_centroid[1])),
            #             radius=3,
            #             color=(0, 0, 255),
            #             thickness=-1,
            #         )
            #         # self.draw_polygon(segment, color=color, edge_color=edge_color, alpha=alpha)

            # semantic classes
            semantic_pred_classes = list(
                item["category_id"] for item in segment_info if "score" not in item
            )
            semantic_class_names = MetadataCatalog.get(
                self.cfg.DATASETS.TRAIN[0]
            ).stuff_classes
            semantic_pred_class_names = list(
                map(lambda x: semantic_class_names[x], semantic_pred_classes)
            )

            return output.get_image()[:, :, ::-1], semantic_pred_class_names
