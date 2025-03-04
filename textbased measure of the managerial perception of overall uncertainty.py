import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

# 下载必要的nltk数据
nltk.download('punkt')
nltk.download('stopwords')

# 定义前瞻性词汇表和不确定性词汇表
forward_looking_words = ["anticipate", "expect", "estimate", "project", "forecast"]
uncertainty_words = ["uncertain", "risk", "uncertainty", "possible", "potential"]
# 定义排除词汇，表明是法律模板内容或提及过去事件的词汇
excluded_words = ["last year", "previous", "in the past"]

# 获取停用词列表
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    文本清洗和预处理函数，去除标点符号和停用词
    """
    # 转换为小写
    text = text.lower()
    # 去除标点符号
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    # 分词
    tokens = word_tokenize(text)
    # 去除停用词
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # 重新组合成文本
    return " ".join(filtered_tokens)

def is_forward_looking_sentence(sentence):
    """
    判断句子是否为前瞻性陈述
    """
    sentence = preprocess_text(sentence)
    words = word_tokenize(sentence)
    for word in forward_looking_words:
        if word in words:
            for excluded in excluded_words:
                if excluded in sentence:
                    return False
            return True
    return False

def is_uncertain_sentence(sentence):
    """
    判断句子是否为不确定的前瞻性陈述
    """
    sentence = preprocess_text(sentence)
    words = word_tokenize(sentence)
    for word in uncertainty_words:
        if word in words:
            return True
    return False

def calculate_fls_uncertainty(text):
    """
    计算前瞻性陈述中的不确定性比例
    """
    # 分句
    sentences = sent_tokenize(text)
    fls_sentences = []
    uncertain_fls_sentences = []

    for sentence in sentences:
        if is_forward_looking_sentence(sentence):
            fls_sentences.append(sentence)
            if is_uncertain_sentence(sentence):
                uncertain_fls_sentences.append(sentence)

    if len(fls_sentences) == 0:
        return 0
    return len(uncertain_fls_sentences) / len(fls_sentences)

def calculate_avg_fls_uc(text_this_year, text_last_year):
    """
    计算两年的平均前瞻性陈述不确定性
    """
    fls_uc_this_year = calculate_fls_uncertainty(text_this_year)
    fls_uc_last_year = calculate_fls_uncertainty(text_last_year)
    return (fls_uc_this_year + fls_uc_last_year) / 2

def convert_to_range_0_1(value, min_value, max_value):
    """
    将值转换到 0 到 1 的范围
    """
    if max_value == min_value:
        return 0
    return (value - min_value) / (max_value - min_value)

# 示例使用
# 假设这里有两个字符串分别代表今年和去年的MD&A文本（到时候你自己换成实际的文本文件）
text_this_year = "We anticipate that our sales will increase next year, but there are some potential risks."
text_last_year = "Last year, we faced some challenges. We expect better results this year with possible market changes."

avg_fls_uc = calculate_avg_fls_uc(text_this_year, text_last_year)

# 假设这里我们有一个样本的最小和最大不确定性值（实际应用中需要根据实际的文本文件计算）
min_uncertainty = 0
max_uncertainty = 1

scaled_uncertainty = convert_to_range_0_1(avg_fls_uc, min_uncertainty, max_uncertainty)
print(f"Average FLS uncertainty: {avg_fls_uc}")
print(f"Scaled FLS uncertainty (0 - 1 range): {scaled_uncertainty}")
