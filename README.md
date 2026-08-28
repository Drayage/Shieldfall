# Shieldfall

모바일 중심 전술 카드 배틀 프로토타입입니다.

- GitHub Pages: https://drayage.github.io/Shieldfall/
- PWA: 브라우저의 **홈 화면에 추가 / 앱 설치** 기능으로 설치할 수 있습니다.
- 오프라인: 최초 접속 후 Service Worker가 게임 셸과 압축된 게임 데이터를 캐시합니다.

## 배포

`main` 브랜치에 push하면 `.github/workflows/deploy-pages.yml`이 GitHub Pages 배포를 실행합니다.

## 구조

- `index.html` — 경량 로더
- `app.gz.b64` — 현재 Shieldfall 게임 HTML을 gzip+base64로 저장한 payload
- `manifest.webmanifest` — PWA manifest
- `sw.js` — 오프라인 캐시
- `icon.svg`, `icon-maskable.svg` — PWA 아이콘
