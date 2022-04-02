## SchoolJoon


[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Friroan%2FSchoolJoon&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com) 
[![Total alerts](https://img.shields.io/lgtm/alerts/g/riroan/SchoolJoon.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/riroan/SchoolJoon/alerts/)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/riroan/SchoolJoon.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/riroan/SchoolJoon/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/riroan/SchoolJoon.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/riroan/SchoolJoon/context:python)
![Lines of code](https://img.shields.io/tokei/lines/github/riroan/SchoolJoon?color=green)
![GitHub last commit](https://img.shields.io/github/last-commit/riroan/SchoolJoon)

특정 학교의 구성원들이 해결한 백준 문제들을 분석하는 프로젝트입니다.

백준 문제들로 다양한 재밌는 기능을 추가할 예정입니다.

일단은 건국대 대상으로 처리할 예정

크롤링할 때 서버에 무리가 가지 않도록 2초 딜레이 설정

(프로젝트명은 임시입니다.)

## 아키텍처 구성

<img src="./images/architecture.PNG" alt="main" width="600" />

## Demo

### 메인페이지
<img src="./images/1.png" alt="main" width="600" />

### 레벨별 미해결 문제
<img src="./images/2.png" alt="main" width="600" />

### 태그별 미해결 문제
<img src="./images/3.png" alt="main" width="600" />

### 특정 레벨 미해결 문제 리스트
<img src="./images/4.png" alt="main" width="600" />

## 기술스택

### FrontEnd

- React(typescript) + scss

- storybook

### BackEnd

- FastAPI(python)

- BeautifulSoup

### Database

- MySQL + PyMySQL
