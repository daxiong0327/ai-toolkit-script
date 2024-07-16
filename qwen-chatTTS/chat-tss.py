# coding=utf-8

import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from natsort import natsorted
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
# 设置 Dashscope API 密钥和 TTS 模型参数
dashscope.api_key = os.getenv('API_KEY')
model = "cosyvoice-v1"
voice = "longyuan"  # 可根据自己的需要进行修改


# 解析 EPUB 文件
def extract_chapters_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text()
            chapters.append(text)

    return chapters


# 将文本拆分为小于或等于 2500 字的块
def split_text_into_chunks(text, max_length=2500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# 将文本转换为音频并保存
def text_to_speech(text, chapter_index, chunk_index, output_folder):
    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call(text)
    request_id = synthesizer.get_last_request_id()
    output_file = os.path.join(output_folder, f'output_chapter_{chapter_index}_part_{chunk_index}.mp3')
    if audio is None:
        print(f'Chapter error: {chapter_index}, Part {chunk_index} failed. Request ID: {request_id}, Text: {text}')
        return
    with open(output_file, 'wb') as f:
        f.write(audio)

    print(f'Chapter {chapter_index}, Part {chunk_index} processed. Request ID: {request_id}')


# 创建章节文件夹并保存文本块
def save_text_chunks(chapter_index, chunks, base_output_folder):
    chapter_folder = os.path.join(base_output_folder, str(chapter_index + 1))
    os.makedirs(chapter_folder, exist_ok=True)

    for chunk_index, chunk in enumerate(chunks):
        text_file = os.path.join(chapter_folder, f'{chunk_index + 1}.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(chunk)


# 从文件中读取文本并转换为语音
def process_text_to_speech(base_output_folder, audio_output_folder):
    chapter_folders = natsorted(os.listdir(base_output_folder))
    for chapter_index in chapter_folders:
        chapter_folder = os.path.join(base_output_folder, chapter_index)
        if os.path.isdir(chapter_folder):
            chunk_files = natsorted(os.listdir(chapter_folder))
            for chunk_file in chunk_files:
                if chunk_file.endswith('.txt'):
                    chunk_index = int(os.path.splitext(chunk_file)[0]) - 1
                    with open(os.path.join(chapter_folder, chunk_file), 'r', encoding='utf-8') as f:
                        text = f.read()
                        text_to_speech(text, chapter_index, chunk_index, audio_output_folder)


# 主函数
def main(epub_path, base_output_folder, audio_output_folder):
    chapters = extract_chapters_from_epub(epub_path)

    for index, chapter in enumerate(chapters):
        chunks = split_text_into_chunks(chapter)
        save_text_chunks(index, chunks, base_output_folder)

    process_text_to_speech(base_output_folder, audio_output_folder)
    save_text_chunks(index, chunks, base_output_folder)


if __name__ == "__main__":
    epub_path = "xiangrikuidi.epub"  # 修改为你的 EPUB 文件路径
    base_output_folder = "../../books/xiangrikuidi_text"  # 修改为你的输出文件夹
    audio_output_folder = "../../books/xiangrikuidi_audio"  # 修改为你的输出文件夹
    main(epub_path, base_output_folder, audio_output_folder)
