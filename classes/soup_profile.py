class SOUP_Profile:
    full_name = ""
    profile_url = ""
    profile_pic = ""
    profile_descriptions = []
    def __init__(self, full_name,profile_url,profile_pic="",profile_descriptions=[]):
        self.profile_url = profile_url
        self.full_name = full_name
        self.profile_pic = profile_pic
        self.profile_descriptions = profile_descriptions