import nltk
from nltk.tokenize import sent_tokenize

# 下载必要的nltk数据
nltk.download('punkt')

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file]
    return words

# 假设这是从i4Semantic算法得到的单位CM和销量相关词汇
# 提取存储在txt文件中的Appendix A Panel A的词
cm_related_words = read_words_from_file('cm_related_words.txt')
volume_related_words = read_words_from_file('volume_related_words.txt')

# 定义前瞻性词汇表和不确定性词汇表
forward_looking_words = ["anticipate", "expect", "estimate", "project", "forecast"]
uncertainty_words = ["uncertain", "risk", "uncertainty", "possible", "potential"]
# 定义排除词汇，表明是法律模板内容或提及过去事件的词汇（自己替换
excluded_words = ["last year", "previous", "in the past"]


def is_forward_looking_sentence(sentence):
    """
    判断句子是否为前瞻性陈述
    """
    for word in forward_looking_words:
        if word in sentence.lower():
            for excluded in excluded_words:
                if excluded in sentence.lower():
                    return False
            return True
    return False


def is_uncertain_sentence(sentence):
    """
    判断句子是否为不确定的前瞻性陈述
    """
    for word in uncertainty_words:
        if word in sentence.lower():
            return True
    return False


def classify_uncertain_fls(text):
    """
    对不确定的FLS句子进行分类
    """
    sentences = sent_tokenize(text)
    cm_uncertain_fls = []
    volume_uncertain_fls = []
    other_uncertain_fls = []

    for sentence in sentences:
        if is_forward_looking_sentence(sentence) and is_uncertain_sentence(sentence):
            is_cm = False
            is_volume = False
            for word in cm_related_words:
                if word in sentence.lower():
                    is_cm = True
                    break
            for word in volume_related_words:
                if word in sentence.lower():
                    is_volume = True
                    break
            if is_cm:
                cm_uncertain_fls.append(sentence)
            elif is_volume:
                volume_uncertain_fls.append(sentence)
            else:
                other_uncertain_fls.append(sentence)

    return cm_uncertain_fls, volume_uncertain_fls, other_uncertain_fls


def calculate_fls_uc(text):
    """
    计算文本中不确定的FLS句子比例
    """
    sentences = sent_tokenize(text)
    fls_sentences = [s for s in sentences if is_forward_looking_sentence(s)]
    uncertain_fls_sentences = [s for s in fls_sentences if is_uncertain_sentence(s)]
    if not fls_sentences:
        return 0
    return len(uncertain_fls_sentences) / len(fls_sentences)


def calculate_uncertainty_metrics(text_this_year, text_last_year):
    """
    计算单位CM、销量和其他不确定性的度量指标
    """
    cm_uncertain_fls_this_year, volume_uncertain_fls_this_year, other_uncertain_fls_this_year = classify_uncertain_fls(
        text_this_year)
    cm_uncertain_fls_last_year, volume_uncertain_fls_last_year, other_uncertain_fls_last_year = classify_uncertain_fls(
        text_last_year)

    total_uncertain_fls_this_year = len(cm_uncertain_fls_this_year) + len(volume_uncertain_fls_this_year) + len(
        other_uncertain_fls_this_year)
    total_uncertain_fls_last_year = len(cm_uncertain_fls_last_year) + len(volume_uncertain_fls_last_year) + len(
        other_uncertain_fls_last_year)

    if total_uncertain_fls_this_year == 0 and total_uncertain_fls_last_year == 0:
        return 0, 0, 0

    cm_ratio_this_year = len(cm_uncertain_fls_this_year) / total_uncertain_fls_this_year if total_uncertain_fls_this_year > 0 else 0
    volume_ratio_this_year = len(volume_uncertain_fls_this_year) / total_uncertain_fls_this_year if total_uncertain_fls_this_year > 0 else 0
    other_ratio_this_year = len(other_uncertain_fls_this_year) / total_uncertain_fls_this_year if total_uncertain_fls_this_year > 0 else 0

    cm_ratio_last_year = len(cm_uncertain_fls_last_year) / total_uncertain_fls_last_year if total_uncertain_fls_last_year > 0 else 0
    volume_ratio_last_year = len(volume_uncertain_fls_last_year) / total_uncertain_fls_last_year if total_uncertain_fls_last_year > 0 else 0
    other_ratio_last_year = len(other_uncertain_fls_last_year) / total_uncertain_fls_last_year if total_uncertain_fls_last_year > 0 else 0

    cm_avg_ratio = (cm_ratio_this_year + cm_ratio_last_year) / 2
    volume_avg_ratio = (volume_ratio_this_year + volume_ratio_last_year) / 2
    other_avg_ratio = (other_ratio_this_year + other_ratio_last_year) / 2

    fls_uc_this_year = calculate_fls_uc(text_this_year)
    fls_uc_last_year = calculate_fls_uc(text_last_year)
    avg_fls_uc = (fls_uc_this_year + fls_uc_last_year) / 2

    uc_unit_cm = cm_avg_ratio * avg_fls_uc
    uc_volume = volume_avg_ratio * avg_fls_uc
    uc_other = other_avg_ratio * avg_fls_uc

    return uc_unit_cm, uc_volume, uc_other


# 示例使用（你换成实际下载的文本文件）
text_this_year = "We anticipate that the price might be uncertain next year. Also, the demand could be volatile."
text_last_year = "We expected some cost uncertainties last year, and the sales quantity was hard to predict."

uc_unit_cm, uc_volume, uc_other = calculate_uncertainty_metrics(text_this_year, text_last_year)
print(f"UC_UnitCM: {uc_unit_cm}")
print(f"UC_Volume: {uc_volume}")
print(f"UC_Other: {uc_other}")
