class HomePage(object):
    login_signup_lbl = "//button[@id='login-button']/span"
    login_signup_btn = "//button[@id='login-button']"

class AuthenticationPanel(object):
    login_create_header = "(//*[@id='left-drawer']//h6)[1]"
    password_login_lbl = "//label[@id='password-login']"
    login_header = "(//*[@id='left-drawer']//h6)[2]"
    username_edit ="username"
    password_edit = "login-pwd"
    submit_btn = "login-submit"
    success_mesg = "//span[contains(text(),'Logged in successfully')]"