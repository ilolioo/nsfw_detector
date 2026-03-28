# config.py
import os
import rarfile
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


def load_config_from_env():
    """从环境变量加载配置

    支持的环境变量:
    - NSFW_THRESHOLD: NSFW检测阈值 (float, 默认0.8)
    - NSFW_MODEL_RESET_THRESHOLD: 鉴黄模型重置阈值 (int)
    - FFMPEG_MAX_FRAMES: FFmpeg最大帧数 (int, 默认20)
    - FFMPEG_MAX_TIMEOUT / FFMPEG_TIMEOUT: FFmpeg超时时间 (int, 默认1800秒)
    - AUTH_TOKEN: API认证Token (string, 默认None)
    - CHECK_ALL_FILES: 是否检查所有文件 (int, 默认0)
    - MAX_INTERVAL_SECONDS: 最大间隔秒数 (int, 默认30)
    - MAX_FILE_SIZE: 最大文件大小 (int, 默认20GB)
    - TAG_MODEL_RESET_THRESHOLD: 标签模型重置阈值 (int)
    - WD_GENERAL_THRESHOLD: WD通用标签阈值 (float, 默认0.32)
    - WD_CHARACTER_THRESHOLD: WD角色标签阈值 (float, 默认0.8)
    - TAG_TOP_K: 自动标签返回数量 (int, 默认8)
    - TAG_MIN_SCORE: 自动标签最小分数阈值 (float, 默认0.2)
    """
    env_config = {}
    env_loaded = {}

    # 定义环境变量映射: 环境变量名 -> (配置键名, 类型转换函数)
    env_mappings = {
        'NSFW_THRESHOLD': ('NSFW_THRESHOLD', float),
        'NSFW_MODEL_RESET_THRESHOLD': ('NSFW_MODEL_RESET_THRESHOLD', int),
        'FFMPEG_MAX_FRAMES': ('FFMPEG_MAX_FRAMES', int),
        'FFMPEG_MAX_TIMEOUT': ('FFMPEG_TIMEOUT', int),  # FFMPEG_MAX_TIMEOUT 映射到 FFMPEG_TIMEOUT
        'FFMPEG_TIMEOUT': ('FFMPEG_TIMEOUT', int),
        'AUTH_TOKEN': ('AUTH_TOKEN', str),
        'CHECK_ALL_FILES': ('CHECK_ALL_FILES', int),
        'MAX_INTERVAL_SECONDS': ('MAX_INTERVAL_SECONDS', int),
        'MAX_FILE_SIZE': ('MAX_FILE_SIZE', int),
        'TAG_MODEL_RESET_THRESHOLD': ('TAG_MODEL_RESET_THRESHOLD', int),
        'WD_GENERAL_THRESHOLD': ('WD_GENERAL_THRESHOLD', float),
        'WD_CHARACTER_THRESHOLD': ('WD_CHARACTER_THRESHOLD', float),
        'TAG_TOP_K': ('TAG_TOP_K', int),
        'TAG_MIN_SCORE': ('TAG_MIN_SCORE', float),
    }

    for env_var, (config_key, type_func) in env_mappings.items():
        value = os.environ.get(env_var)
        if value is not None:
            try:
                # 特殊处理AUTH_TOKEN: 空字符串视为None
                if config_key == 'AUTH_TOKEN':
                    if value.strip() == '':
                        env_config[config_key] = None
                    else:
                        env_config[config_key] = value.strip()
                else:
                    env_config[config_key] = type_func(value)
                env_loaded[env_var] = env_config[config_key]
            except ValueError as e:
                logger.warning(f"环境变量 {env_var} 的值 '{value}' 无法转换为 {type_func.__name__}: {e}")

    return env_config, env_loaded

# 基础配置
rarfile.UNRAR_TOOL = "unrar"
rarfile.PATH_SEP = '/'
os.environ['HF_HOME'] = '/root/.cache/huggingface'

# MIME类型到文件扩展名的映射
# config.py 中的 MIME_TO_EXT 字典应该这样修改：

# MIME类型到文件扩展名的映射
MIME_TO_EXT = {
    # 图片格式
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    'image/bmp': '.bmp',
    'image/tiff': '.tiff',
    'image/x-tiff': '.tiff',
    'image/x-tga': '.tga',
    'image/x-portable-pixmap': '.ppm',
    'image/x-portable-graymap': '.pgm',
    'image/x-portable-bitmap': '.pbm',
    'image/x-portable-anymap': '.pnm',
    'image/svg+xml': '.svg',
    'image/x-pcx': '.pcx',
    'image/vnd.adobe.photoshop': '.psd',
    'image/vnd.microsoft.icon': '.ico',
    'image/heif': '.heif',
    'image/heic': '.heic',
    'image/avif': '.avif',
    'image/jxl': '.jxl',

    # PDF格式
    'application/pdf': '.pdf',

    # 文档格式 (新增)
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',

    # 视频和容器格式
    'video/mp4': '.mp4',
    'video/x-msvideo': '.avi',
    'video/x-matroska': '.mkv',
    'video/quicktime': '.mov',
    'video/x-ms-wmv': '.wmv',
    'video/webm': '.webm',
    'video/MP2T': '.ts',
    'video/x-flv': '.flv',
    'video/3gpp': '.3gp',
    'video/3gpp2': '.3g2',
    'video/x-m4v': '.m4v',
    'video/mxf': '.mxf',
    'video/x-ogm': '.ogm',
    'video/vnd.rn-realvideo': '.rv',
    'video/dv': '.dv',
    'video/x-ms-asf': '.asf',
    'video/x-f4v': '.f4v',
    'video/vnd.dlna.mpeg-tts': '.m2ts',
    'video/x-raw': '.yuv',
    'video/mpeg': '.mpg',
    'video/x-mpeg': '.mpeg',
    'video/divx': '.divx',
    'video/x-vob': '.vob',
    'video/x-m2v': '.m2v',

    # 压缩格式
    'application/x-rar-compressed': '.rar',
    'application/x-rar': '.rar',
    'application/vnd.rar': '.rar',
    'application/zip': '.zip',
    'application/x-7z-compressed': '.7z',
    'application/gzip': '.gz',
    'application/x-tar': '.tar',
    'application/x-bzip2': '.bz2',
    'application/x-xz': '.xz',
    'application/x-lzma': '.lzma',
    'application/x-zstd': '.zst',
    'application/vnd.ms-cab-compressed': '.cab'
}

# 文件扩展名集合
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tga',
                   '.ppm', '.pgm', '.pbm', '.pnm', '.svg', '.pcx', '.psd', '.ico',
                   '.heif', '.heic', '.avif', '.jxl'}

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.webm', '.ts', '.flv',
                   '.3gp', '.3g2', '.m4v', '.mxf', '.ogm', '.rv', '.dv', '.asf',
                   '.f4v', '.m2ts', '.yuv', '.mpg', '.mpeg', '.divx', '.vob', '.m2v'}

ARCHIVE_EXTENSIONS = {'.7z', '.rar', '.zip', '.gz', '.tar', '.bz2', '.xz',
                     '.lzma', '.zst', '.cab'}

# 添加新的文档扩展名集合
DOCUMENT_EXTENSIONS = {'.doc', '.docx'}

# 添加新的 MIME 类型集合
DOCUMENT_MIME_TYPES = {
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

# MIME 类型集合
IMAGE_MIME_TYPES = {mime for mime, ext in MIME_TO_EXT.items() if mime.startswith('image/')}
VIDEO_MIME_TYPES = {mime for mime, ext in MIME_TO_EXT.items() if mime.startswith('video/')}
ARCHIVE_MIME_TYPES = {mime for mime, ext in MIME_TO_EXT.items() if
    mime.startswith('application/') and
    any(keyword in mime for keyword in ['zip', 'rar', '7z', 'gzip', 'tar',
        'bzip2', 'xz', 'lzma', 'zstd', 'cab'])}
PDF_MIME_TYPES = {'application/pdf'}

# 所有支持的 MIME 类型集合
SUPPORTED_MIME_TYPES = IMAGE_MIME_TYPES | VIDEO_MIME_TYPES | ARCHIVE_MIME_TYPES | PDF_MIME_TYPES | DOCUMENT_MIME_TYPES

# 默认配置值
MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024  # 20GB
NSFW_THRESHOLD = 0.8
NSFW_MODEL_NAME = 'Freepik/nsfw_image_detector'
NSFW_MODEL_RESET_THRESHOLD = 10000
FFMPEG_MAX_FRAMES = 20
FFMPEG_TIMEOUT = 1800
CHECK_ALL_FILES = 0
MAX_INTERVAL_SECONDS = 30
AUTH_TOKEN = None  # API认证Token，设置后需要在请求头中携带Token
TAG_MODEL_NAME = 'SmilingWolf/wd-vit-tagger-v3'
TAG_MODEL_RESET_THRESHOLD = 5000
WD_GENERAL_THRESHOLD = 0.32
WD_CHARACTER_THRESHOLD = 0.80
TAG_TOP_K = 10
TAG_MIN_SCORE = 0.15

BROAD_TAG_LABELS = {
    'anime': '动漫',
    'manga': '漫画',
    'girl': '少女',
    'yuri': '百合',
    'loli': '萝莉',
    'maid': '女仆',
    'idol': '偶像',
    'school_uniform': '校服',
    'kemonomimi': '兽耳',
    'duo': '双人',
    'group': '多人',
    'couple': '情侣',
    'woman': '女性',
    'man': '男性',
    'animal': '动物',
    'pet': '宠物',
    'landscape': '风景',
    'indoor': '室内',
    'outdoor': '户外',
    'city': '城市',
    'building': '建筑',
    'school': '校园',
    'bedroom': '卧室',
    'bathroom': '浴室',
    'stage': '舞台',
    'beach': '海边',
    'forest': '森林',
    'mountain': '山景',
    'food': '食物',
    'drink': '饮品',
    'product': '商品',
    'logo': '标志',
    'interface': '界面',
    'document': '文档',
    'chart': '图表',
    'game': '游戏',
    'night': '夜景',
    'vehicle': '交通工具',
    'fashion': '时尚',
    'beauty': '美妆',
    'cosplay': 'Cosplay',
    'swimwear': '泳装',
    'poster': '海报',
    'advertisement': '广告',
    'packaging': '包装',
    'webpage': '网页',
    'avatar': '头像',
    'cover': '封面',
    'wallpaper': '壁纸',
    'meme': '表情包',
    'bare_feet': '玉足',
    'white_stockings': '白丝',
    'black_stockings': '黑丝',
    'other': '其他'
}

TAG_LABELS = [
    {'key': 'anime', 'label': '动漫', 'hypothesis': 'anime art'},
    {'key': 'manga', 'label': '漫画', 'hypothesis': 'manga style'},
    {'key': 'landscape', 'label': '风景', 'hypothesis': 'landscape'},
    {'key': 'girl', 'label': '少女', 'hypothesis': 'girl'},
    {'key': 'loli', 'label': '萝莉', 'hypothesis': 'loli anime girl'},
    {'key': 'cute_girl', 'label': '可爱少女', 'hypothesis': 'cute girl'},
    {'key': 'woman', 'label': '女性', 'hypothesis': 'woman'},
    {'key': 'man', 'label': '男性', 'hypothesis': 'man'},
    {'key': 'portrait', 'label': '人像', 'hypothesis': 'portrait'},
    {'key': 'close_up_face', 'label': '面部特写', 'hypothesis': 'close-up face'},
    {'key': 'full_body', 'label': '全身像', 'hypothesis': 'full body portrait'},
    {'key': 'selfie', 'label': '自拍', 'hypothesis': 'selfie photo'},
    {'key': 'long_hair', 'label': '长发', 'hypothesis': 'long hair'},
    {'key': 'short_hair', 'label': '短发', 'hypothesis': 'short hair'},
    {'key': 'twintails', 'label': '双马尾', 'hypothesis': 'twintails hairstyle'},
    {'key': 'school_uniform', 'label': '校服', 'hypothesis': 'school uniform'},
    {'key': 'maid_outfit', 'label': '女仆装', 'hypothesis': 'maid outfit'},
    {'key': 'cosplay', 'label': 'Cosplay', 'hypothesis': 'cosplay costume'},
    {'key': 'dress', 'label': '连衣裙', 'hypothesis': 'dress outfit'},
    {'key': 'swimwear', 'label': '泳装', 'hypothesis': 'swimwear'},
    {'key': 'lingerie', 'label': '内衣', 'hypothesis': 'lingerie'},
    {'key': 'stockings', 'label': '丝袜', 'hypothesis': 'stockings'},
    {'key': 'white_stockings', 'label': '白丝', 'hypothesis': 'white stockings'},
    {'key': 'black_stockings', 'label': '黑丝', 'hypothesis': 'black stockings'},
    {'key': 'pantyhose', 'label': '连裤袜', 'hypothesis': 'pantyhose'},
    {'key': 'thighhighs', 'label': '过膝袜', 'hypothesis': 'thighhighs'},
    {'key': 'knee_high_socks', 'label': '及膝袜', 'hypothesis': 'knee high socks'},
    {'key': 'garter_straps', 'label': '吊带袜', 'hypothesis': 'garter straps'},
    {'key': 'ankle_socks', 'label': '短袜', 'hypothesis': 'ankle socks'},
    {'key': 'long_socks', 'label': '长筒袜', 'hypothesis': 'long socks'},
    {'key': 'leggings', 'label': '打底裤', 'hypothesis': 'leggings'},
    {'key': 'bare_legs', 'label': '裸腿', 'hypothesis': 'bare legs'},
    {'key': 'bare_shoulders', 'label': '露肩', 'hypothesis': 'bare shoulders'},
    {'key': 'legs', 'label': '美腿', 'hypothesis': 'beautiful legs'},
    {'key': 'bare_feet', 'label': '玉足', 'hypothesis': 'bare feet focus'},
    {'key': 'midriff', 'label': '露腰', 'hypothesis': 'midriff exposed'},
    {'key': 'cleavage', 'label': '胸部特写', 'hypothesis': 'cleavage focus'},
    {'key': 'outdoor', 'label': '户外', 'hypothesis': 'outdoor scene'},
    {'key': 'indoor', 'label': '室内', 'hypothesis': 'indoor scene'},
    {'key': 'nature', 'label': '自然', 'hypothesis': 'nature'},
    {'key': 'bedroom', 'label': '卧室', 'hypothesis': 'bedroom scene'},
    {'key': 'bathroom', 'label': '浴室', 'hypothesis': 'bathroom scene'},
    {'key': 'classroom', 'label': '教室', 'hypothesis': 'classroom scene'},
    {'key': 'stage', 'label': '舞台', 'hypothesis': 'stage performance'},
    {'key': 'mountain', 'label': '山脉', 'hypothesis': 'mountain'},
    {'key': 'forest', 'label': '森林', 'hypothesis': 'forest'},
    {'key': 'beach', 'label': '海滩', 'hypothesis': 'beach'},
    {'key': 'sky', 'label': '天空', 'hypothesis': 'sky'},
    {'key': 'city', 'label': '城市', 'hypothesis': 'cityscape'},
    {'key': 'building', 'label': '建筑', 'hypothesis': 'building'},
    {'key': 'car', 'label': '汽车', 'hypothesis': 'car'},
    {'key': 'animal', 'label': '动物', 'hypothesis': 'animal'},
    {'key': 'pet', 'label': '宠物', 'hypothesis': 'pet'},
    {'key': 'bird', 'label': '鸟类', 'hypothesis': 'bird'},
    {'key': 'flower', 'label': '花卉', 'hypothesis': 'flower'},
    {'key': 'food', 'label': '食物', 'hypothesis': 'food'},
    {'key': 'drink', 'label': '饮品', 'hypothesis': 'drink'},
    {'key': 'illustration', 'label': '插画', 'hypothesis': 'illustration'},
    {'key': 'cartoon', 'label': '卡通', 'hypothesis': 'cartoon'},
    {'key': 'brand', 'label': '品牌元素', 'hypothesis': 'brand design'},
    {'key': 'logo', 'label': 'Logo', 'hypothesis': 'logo'},
    {'key': 'icon', 'label': '图标', 'hypothesis': 'icon'},
    {'key': 'poster', 'label': '海报', 'hypothesis': 'poster design'},
    {'key': 'banner', 'label': '横幅', 'hypothesis': 'promotional banner'},
    {'key': 'advertisement', 'label': '广告素材', 'hypothesis': 'advertisement design'},
    {'key': 'user_interface', 'label': '界面', 'hypothesis': 'user interface'},
    {'key': 'app_interface', 'label': '应用界面', 'hypothesis': 'mobile app interface'},
    {'key': 'webpage', 'label': '网页', 'hypothesis': 'web page screenshot'},
    {'key': 'screenshot', 'label': '截图', 'hypothesis': 'screen capture'},
    {'key': 'text', 'label': '文字', 'hypothesis': 'text content'},
    {'key': 'document_page', 'label': '文档页', 'hypothesis': 'document page'},
    {'key': 'chart', 'label': '图表', 'hypothesis': 'data chart'},
    {'key': 'infographic', 'label': '信息图', 'hypothesis': 'infographic'},
    {'key': 'product', 'label': '商品图', 'hypothesis': 'product photo'},
    {'key': 'packaging', 'label': '产品包装', 'hypothesis': 'product packaging'},
    {'key': 'fashion', 'label': '时尚', 'hypothesis': 'fashion photo'},
    {'key': 'beauty', 'label': '美妆', 'hypothesis': 'beauty product'},
    {'key': 'meme', 'label': '表情包', 'hypothesis': 'internet meme'},
    {'key': 'game', 'label': '游戏画面', 'hypothesis': 'video game screenshot'},
    {'key': 'vehicle', 'label': '交通工具', 'hypothesis': 'vehicle'},
    {'key': 'monochrome', 'label': '黑白画面', 'hypothesis': 'monochrome image'},
    {'key': 'idol', 'label': '偶像风', 'hypothesis': 'idol style'},
    {'key': 'night', 'label': '夜景', 'hypothesis': 'night scene'},
    {'key': 'other', 'label': '其他', 'hypothesis': 'other'}
]

TAG_DERIVED_RELATIONS = {
    'anime': ['illustration', 'cartoon'],
    'manga': ['illustration', 'cartoon'],
    'logo': ['icon', 'brand'],
    'icon': ['brand'],
    'poster': ['advertisement'],
    'banner': ['advertisement'],
    'user_interface': ['screenshot'],
    'app_interface': ['user_interface', 'screenshot'],
    'webpage': ['screenshot', 'text'],
    'document_page': ['text'],
    'chart': ['infographic', 'text'],
    'product': ['packaging'],
    'fashion': ['beauty'],
    'girl': ['portrait'],
    'woman': ['portrait'],
    'man': ['portrait'],
    'loli': ['girl', 'anime'],
    'cute_girl': ['girl', 'portrait'],
    'pet': ['animal'],
    'bird': ['animal'],
    'flower': ['nature'],
    'mountain': ['landscape', 'nature'],
    'forest': ['landscape', 'nature'],
    'beach': ['landscape', 'outdoor'],
    'city': ['building'],
    'car': ['vehicle'],
    'game': ['screenshot'],
    'meme': ['text']
}

WD_TAG_ALIASES = {
    'anime': ['anime', 'anime coloring', 'anime screencap', 'cel shading'],
    'manga': ['manga', 'comic'],
    'landscape': ['landscape', 'scenery'],
    'girl': ['1girl', 'girl', 'female focus', 'solo female'],
    'loli': ['loli'],
    'cute_girl': ['cute girl'],
    'woman': ['woman', 'female'],
    'man': ['1boy', 'boy', 'man', 'male focus'],
    'portrait': ['portrait', 'upper body', 'cowboy shot'],
    'close_up_face': ['close-up', 'face focus', 'close up'],
    'full_body': ['full body', 'standing'],
    'selfie': ['selfie'],
    'long_hair': ['long hair'],
    'short_hair': ['short hair'],
    'twintails': ['twintails'],
    'school_uniform': ['school uniform'],
    'maid_outfit': ['maid', 'maid headdress', 'maid outfit'],
    'cosplay': ['cosplay'],
    'dress': ['dress'],
    'swimwear': ['swimsuit', 'bikini', 'one-piece swimsuit', 'school swimsuit', 'swimwear'],
    'lingerie': ['lingerie', 'bra', 'panties'],
    'stockings': ['stockings'],
    'white_stockings': ['white stockings', 'white thighhighs', 'white legwear'],
    'black_stockings': ['black stockings', 'black thighhighs', 'black legwear'],
    'pantyhose': ['pantyhose'],
    'thighhighs': ['thighhighs', 'thigh-highs'],
    'knee_high_socks': ['kneehighs', 'knee high socks'],
    'garter_straps': ['garter straps'],
    'ankle_socks': ['ankle socks'],
    'long_socks': ['long socks'],
    'leggings': ['leggings'],
    'bare_legs': ['bare legs'],
    'bare_shoulders': ['bare shoulders'],
    'legs': ['legs', 'beautiful legs'],
    'bare_feet': ['barefoot', 'bare feet', 'feet'],
    'midriff': ['midriff'],
    'cleavage': ['cleavage'],
    'outdoor': ['outdoors', 'outdoor'],
    'indoor': ['indoors', 'indoor'],
    'nature': ['nature'],
    'bedroom': ['bedroom'],
    'bathroom': ['bathroom'],
    'classroom': ['classroom'],
    'stage': ['stage'],
    'mountain': ['mountain'],
    'forest': ['forest'],
    'beach': ['beach'],
    'sky': ['sky'],
    'city': ['city', 'cityscape'],
    'building': ['building'],
    'car': ['car'],
    'animal': ['animal'],
    'pet': ['pet'],
    'bird': ['bird'],
    'flower': ['flower'],
    'food': ['food'],
    'drink': ['drink'],
    'illustration': ['illustration'],
    'cartoon': ['cartoon'],
    'brand': ['brand', 'brand name'],
    'logo': ['logo'],
    'icon': ['icon'],
    'poster': ['poster'],
    'banner': ['banner'],
    'advertisement': ['advertisement', 'ad'],
    'user_interface': ['user interface', 'ui'],
    'app_interface': ['mobile ui', 'app ui', 'mobile app interface'],
    'webpage': ['web page', 'website'],
    'screenshot': ['screenshot', 'screen capture'],
    'text': ['text', 'english text'],
    'document_page': ['document page'],
    'chart': ['chart', 'graph'],
    'infographic': ['infographic'],
    'product': ['product', 'product photo'],
    'packaging': ['packaging', 'product packaging'],
    'fashion': ['fashion'],
    'beauty': ['beauty product', 'makeup'],
    'meme': ['meme', 'internet meme'],
    'game': ['video game', 'video game screenshot', 'game cg'],
    'vehicle': ['vehicle'],
    'monochrome': ['monochrome', 'greyscale'],
    'idol': ['idol'],
    'night': ['night', 'night scene']
}

WD_BROAD_TAG_ALIASES = {
    'anime': ['anime', 'anime coloring', 'anime screencap', 'cel shading', 'illustration', 'cartoon'],
    'manga': ['manga', 'comic'],
    'girl': ['1girl', 'girl', 'female focus', 'solo female', 'cute girl'],
    'yuri': ['yuri', 'girls love', '2girls', 'multiple girls'],
    'loli': ['loli'],
    'maid': ['maid', 'maid headdress', 'maid outfit'],
    'idol': ['idol'],
    'school_uniform': ['school uniform'],
    'kemonomimi': ['animal ears', 'cat ears', 'fox ears', 'bunny ears'],
    'duo': ['2girls', '2boys', '1girl 1boy', 'duo'],
    'group': ['multiple girls', 'multiple boys', 'group picture', 'crowd'],
    'couple': ['couple', 'holding hands', 'hug'],
    'woman': ['woman', 'female'],
    'man': ['1boy', 'boy', 'man', 'male focus'],
    'animal': ['animal', 'pet', 'bird'],
    'pet': ['pet'],
    'landscape': ['landscape', 'scenery', 'nature', 'outdoors', 'mountain', 'forest', 'beach', 'sky'],
    'indoor': ['indoors', 'indoor'],
    'outdoor': ['outdoors', 'outdoor'],
    'city': ['city', 'cityscape'],
    'building': ['building'],
    'school': ['school uniform', 'classroom'],
    'bedroom': ['bedroom'],
    'bathroom': ['bathroom'],
    'stage': ['stage', 'idol'],
    'beach': ['beach'],
    'forest': ['forest'],
    'mountain': ['mountain'],
    'food': ['food', 'drink'],
    'drink': ['drink'],
    'product': ['product', 'product photo', 'product packaging'],
    'logo': ['logo', 'icon', 'brand', 'brand name'],
    'interface': ['user interface', 'ui', 'mobile ui', 'app ui', 'mobile app interface', 'web page', 'website', 'screenshot', 'screen capture', 'document page', 'chart', 'graph', 'infographic', 'text', 'english text'],
    'document': ['document page', 'text', 'english text'],
    'chart': ['chart', 'graph', 'infographic'],
    'game': ['video game', 'video game screenshot', 'game cg'],
    'night': ['night', 'night scene'],
    'vehicle': ['vehicle', 'car'],
    'fashion': ['fashion', 'dress'],
    'beauty': ['beauty product', 'makeup'],
    'cosplay': ['cosplay', 'maid', 'maid headdress', 'maid outfit'],
    'swimwear': ['swimsuit', 'bikini', 'one-piece swimsuit', 'school swimsuit', 'swimwear'],
    'poster': ['poster'],
    'advertisement': ['advertisement', 'ad', 'promotional banner', 'banner'],
    'packaging': ['packaging', 'product packaging'],
    'webpage': ['web page', 'website'],
    'avatar': ['profile picture', 'avatar'],
    'cover': ['cover', 'album cover', 'book cover'],
    'wallpaper': ['wallpaper'],
    'meme': ['meme', 'internet meme'],
    'bare_feet': ['barefoot', 'bare feet', 'feet'],
    'white_stockings': ['white stockings', 'white thighhighs', 'white legwear'],
    'black_stockings': ['black stockings', 'black thighhighs', 'black legwear']
}

# 从环境变量加载配置
env_config, env_loaded = load_config_from_env()

# 更新全局变量
globals().update(env_config)

# 记录生效的配置
logger.info("当前生效的配置:")
logger.info("-" * 50)
final_nsfw = env_config.get('NSFW_THRESHOLD', NSFW_THRESHOLD)
final_nsfw_model = env_config.get('NSFW_MODEL_NAME', NSFW_MODEL_NAME)
final_nsfw_reset = env_config.get('NSFW_MODEL_RESET_THRESHOLD', NSFW_MODEL_RESET_THRESHOLD)
final_frames = env_config.get('FFMPEG_MAX_FRAMES', FFMPEG_MAX_FRAMES)
final_timeout = env_config.get('FFMPEG_TIMEOUT', FFMPEG_TIMEOUT)
final_token = env_config.get('AUTH_TOKEN', AUTH_TOKEN)
final_tag_model = env_config.get('TAG_MODEL_NAME', TAG_MODEL_NAME)
final_tag_reset = env_config.get('TAG_MODEL_RESET_THRESHOLD', TAG_MODEL_RESET_THRESHOLD)
final_wd_general_threshold = env_config.get('WD_GENERAL_THRESHOLD', WD_GENERAL_THRESHOLD)
final_wd_character_threshold = env_config.get('WD_CHARACTER_THRESHOLD', WD_CHARACTER_THRESHOLD)
logger.info(f"{'NSFW_THRESHOLD':25s} = {final_nsfw}")
logger.info(f"{'NSFW_MODEL_NAME':25s} = {final_nsfw_model}")
logger.info(f"{'NSFW_MODEL_RESET_THRESHOLD':25s} = {final_nsfw_reset}")
logger.info(f"{'FFMPEG_MAX_FRAMES':25s} = {final_frames}")
logger.info(f"{'FFMPEG_TIMEOUT':25s} = {final_timeout}")
logger.info(f"{'AUTH_TOKEN':25s} = {'***' if final_token else 'None'}")
logger.info(f"{'TAG_MODEL_NAME':25s} = {final_tag_model}")
logger.info(f"{'TAG_MODEL_RESET_THRESHOLD':25s} = {final_tag_reset}")
logger.info(f"{'WD_GENERAL_THRESHOLD':25s} = {final_wd_general_threshold}")
logger.info(f"{'WD_CHARACTER_THRESHOLD':25s} = {final_wd_character_threshold}")
logger.info(f"{'TAG_TOP_K':25s} = {env_config.get('TAG_TOP_K', TAG_TOP_K)}")
logger.info(f"{'TAG_MIN_SCORE':25s} = {env_config.get('TAG_MIN_SCORE', TAG_MIN_SCORE)}")
if env_loaded:
    logger.info("-" * 50)
    logger.info("以上配置来自环境变量覆盖")

# 导出所有配置变量
__all__ = [
    'MIME_TO_EXT', 'IMAGE_EXTENSIONS', 'VIDEO_EXTENSIONS', 'ARCHIVE_EXTENSIONS',
    'DOCUMENT_EXTENSIONS',  # 新增
    'IMAGE_MIME_TYPES', 'VIDEO_MIME_TYPES', 'ARCHIVE_MIME_TYPES', 'PDF_MIME_TYPES',
    'DOCUMENT_MIME_TYPES',  # 新增
    'SUPPORTED_MIME_TYPES', 'MAX_FILE_SIZE', 'NSFW_THRESHOLD', 'FFMPEG_MAX_FRAMES',
    'FFMPEG_TIMEOUT', 'CHECK_ALL_FILES', 'MAX_INTERVAL_SECONDS', 'AUTH_TOKEN',
    'NSFW_MODEL_NAME', 'NSFW_MODEL_RESET_THRESHOLD',
    'TAG_MODEL_NAME', 'TAG_MODEL_RESET_THRESHOLD',
    'WD_GENERAL_THRESHOLD', 'WD_CHARACTER_THRESHOLD',
    'TAG_TOP_K', 'TAG_MIN_SCORE', 'TAG_LABELS', 'TAG_DERIVED_RELATIONS', 'WD_TAG_ALIASES',
    'BROAD_TAG_LABELS', 'WD_BROAD_TAG_ALIASES'
]
