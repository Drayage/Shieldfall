# Shieldfall

모바일 중심 전술 카드 배틀 프로토타입입니다.

- GitHub Pages: https://drayage.github.io/Shieldfall/
- PWA: 지원 브라우저의 **앱 설치 / 홈 화면에 추가** 기능으로 설치할 수 있습니다.
- 오프라인: 최초 로드 뒤 Service Worker가 게임 셸과 게임 payload를 캐시합니다.

## 배포

`main` 브랜치에 push하면 `.github/workflows/deploy-pages.yml`이 GitHub Pages 배포를 실행합니다.

## 구조

- `index.html` — 경량 게임 로더
- `app/chunk00.b64` ~ `app/chunk07.b64` — 현재 Shieldfall HTML의 gzip+base64 payload
- `manifest.webmanifest` — PWA manifest
- `sw.js` — 오프라인 캐시
- `icon.svg`, `icon-maskable.svg` — PWA 아이콘
- `.github/workflows/deploy-pages.yml` — GitHub Pages 배포

게임을 수정할 때는 원본 단일 HTML을 수정한 뒤 gzip+base64 payload를 다시 생성해 8개 chunk로 갱신하면 됩니다.
