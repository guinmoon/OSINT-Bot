from python3_anticaptcha import  ImageToTextTask

anticaptcha_key = 'de7e627a5c54cbf6e33c72cb90d904a3'
user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = anticaptcha_key).captcha_handler(captcha_file='./captcha/bIywEhbrkV.jpg')
print(user_answer)
