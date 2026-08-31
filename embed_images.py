import base64
import os

def update_html():
    b64_map = {}
    for i in range(1, 6):
        with open(f'카드뉴스{i}.png', 'rb') as f:
            b64_map[i] = f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'

    with open('배포/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    for i in range(1, 6):
        # 교체 1: img 태그
        target_img = f'<img src="카드뉴스{i}.png"'
        if target_img in content:
            content = content.replace(target_img, f'<img src="{b64_map[i]}"')
        
        # 교체 2: lightbox 호출
        target_lightbox = f"openLightbox('카드뉴스{i}.png'"
        if target_lightbox in content:
            content = content.replace(target_lightbox, f"openLightbox(cardNewsImages[{i}]")

    # JS 객체 삽입
    js_snippet = "    // 카드뉴스 Base64 이미지 맵\n    const cardNewsImages = {\n"
    for i in range(1, 6):
        js_snippet += f'      {i}: "{b64_map[i]}",\n'
    js_snippet += "    };\n\n"

    if "const cardNewsImages" not in content:
        content = content.replace('// 모집공고 원본 데이터', js_snippet + '    // 모집공고 원본 데이터')

    with open('배포/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("index.html 업데이트 완료: Base64 이미지 5종이 완벽하게 인라인 임베드되었습니다.")

if __name__ == "__main__":
    update_html()
