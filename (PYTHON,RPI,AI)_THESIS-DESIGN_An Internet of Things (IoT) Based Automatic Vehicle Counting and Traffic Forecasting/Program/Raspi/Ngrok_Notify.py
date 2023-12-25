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
    cmd = "/home/pi/ngrok tcp 5000 --log=stdout"
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline().strip()
        if line.find("started tunnel") != -1:
            print(line)
            sendemail(
                "thesistrafficforecasting@gmail.com",
                ["thesistrafficforecasting@gmail.com"],
                "Ngrok Notify",
                line,
                "thesistrafficforecasting@gmail.com",
                "fzkyxqphtbccnqiu",
            )
