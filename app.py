import streamlit as st
import requests
from bs4 import BeautifulSoup

# 웹사이트 제목 설정
st.title("🇰🇷 대한민국 IT / 백엔드 채용 공고 모음")
st.write("원티드(Wanted)에서 실시간으로 신입 및 개발자 공고를 모아 보여줍니다.")

# 검색어 입력창 만들기
keyword = st.text_input("찾고 싶은 포지션이나 키워드를 입력하세요 (예: 백엔드, 프론트엔드, 신입)", "백엔드 신입")

if st.button("공고 검색하기"):
    with st.spinner("채용 공고를 불러오는 중입니다..."):
        # 검색어를 URL에 맞게 변환
        target_url = f"https://www.wanted.co.kr/search?query={keyword}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            response = requests.get(target_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            notices = []
            for item in soup.find_all('a', href=True):
                title = item.get_text().strip()
                link = item.get("href", "")
                
                if len(title) > 10 and ("채용" in title or "개발" in title or "엔지니어" in title):
                    if link.startswith("/"):
                        link = "https://www.wanted.co.kr" + link
                    
                    if {"title": title, "link": link} not in notices:
                        notices.append({"title": title, "link": link})
                
                if len(notices) >= 10: # 최대 10개 표시
                    break
            
            if notices:
                st.success(f"총 {len(notices)}개의 공고를 찾았습니다!")
                for n in notices:
                    st.markdown(f"### [{n['title']}]({n['link']})")
                    st.write(f"👉 [공고 바로가기 링크]({n['link']})")
                    st.divider()
            else:
                st.warning("조건에 맞는 공고를 찾지 못했습니다.")
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
