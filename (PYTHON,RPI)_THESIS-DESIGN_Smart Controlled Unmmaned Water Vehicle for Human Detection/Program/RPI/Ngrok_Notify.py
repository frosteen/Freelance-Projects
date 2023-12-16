import smtplib
import subprocess
import time

time.sleep(5)


def sendemail(FROM, TO, SUBJECT, TEXT, EMAIL, PASSWORD):
    message = """
From: %s
To: %s
Subject: %s

%s
	""" % (
        FROM,
        ", ".join(TO),
        SUBJECT,
        TEXT,
    )
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(FROM, TO, message)
    server.quit()


if __name__ == "__main__":
    cmd = "/home/pi/ngrok http 8080 --log=stdout"
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    while True:
        line_with_ngrok_url = p.stdout.readline().strip().decode("utf-8")
        if line_with_ngrok_url.find("started tunnel") != -1:
            url_only = line_with_ngrok_url[
                line_with_ngrok_url.index("url=") + len("url=") :
            ]
            print(url_only)
            sendemail(
                "unmanned.vehicle.2022@gmail.com",
                ["unmanned.vehicle.2022@gmail.com"],
                "Ngrok Notify",
                url_only,
                "unmanned.vehicle.2022@gmail.com",
                "czkswzrvulvmkhvu",
            )
