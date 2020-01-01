class RuleBuilder:
    TAG_NORMAL = 'normal'  # 正常
    TAG_PORN = 'pron'  # 性感
    TAG_HOT = 'hot'  # 黄色图像
    TAG_FEMALE_GENITAL = 'female-genital'  # 女性阴部
    TAG_FEMALE_BREAST = 'female-breast'  # 女性胸部
    TAG_MALE_GENITAL = 'male-genital'  # 男性阴部
    TAG_PUBES = 'pubes'  # 阴毛
    TAG_ANUS = 'anus'  # 肛门
    TAG_SEX = 'sex'  # 性行为
    TAG_NORMAL_HOT_PORN = 'normal_hot_porn'  # 图像为色情的综合值

    class Punishment:
        @staticmethod
        def kick(reject_add_request):
            return {'p': 'kick', 'reject': reject_add_request}

        @staticmethod
        def ban(times):
            return {'p': 'ban', 'times': times}

    def __init__(self):
        self.rules = []

    def add(self, tag_name, tag_min, tag_max, delete_message, punishment):
        self.rules.append({
            'tag_name': tag_name,
            'tag_min': tag_min,
            'tag_max': tag_max,
            'delete_message': delete_message,
            'punishment': punishment
        })
        return self

    def build(self):
        return self.rules
