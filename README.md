# Shieldfall

모바일 중심 전술 카드 배틀 프로토타입입니다.

- GitHub Pages: `https://drayage.github.io/Shieldfall/`
- PWA: 지원 브라우저의 **앱 설치 / 홈 화면에 추가** 기능으로 설치할 수 있습니다.
- 오프라인: 최초 접속 후 Service Worker가 게임 본체와 PWA 셸을 캐시합니다.

## 최초 1회: GitHub Pages 활성화

새 저장소에서는 Pages를 한 번 활성화해야 합니다.

1. 저장소 **Settings → Pages**로 이동
2. **Build and deployment → Source**를 **GitHub Actions**로 선택
3. 저장
4. **Actions → Deploy Shieldfall to GitHub Pages**에서 실패한 최신 실행을 **Re-run all jobs** 하거나 `main`에 새 커밋을 push

그 뒤부터는 `main` 브랜치에 push할 때마다 자동 배포됩니다.

## 배포 구조

`.github/workflows/deploy-pages.yml`이 다음 순서로 배포합니다.

1. `scripts/build_pages.py` 실행
2. gzip+base64 payload를 원본 Shieldfall HTML로 복원
3. SHA-256 체크섬으로 원본 일치 여부 검증
4. `_site/index.html`과 PWA 파일 생성
5. GitHub Pages에 `_site` 배포

현재 검증 대상 HTML SHA-256:

`6df9ea3f4e9bd5cfe290cae1c8b11169a55cf1fe079c7780ee899a778db5a7c2`

## 저장소 구조

- `index.html` — 저장소 직접 서빙용 경량 로더
- `app/chunk00.b64`
- `app/chunk01a.b64`, `app/chunk01b.b64`
- `app/chunk02.b64` ~ `app/chunk07.b64`
- `scripts/build_pages.py` — Pages용 완성 HTML 생성 및 체크섬 검증
- `manifest.webmanifest` — PWA manifest
- `sw.js` — 오프라인 캐시 Service Worker
- `icon.svg`, `icon-maskable.svg` — PWA 아이콘
- `.github/workflows/deploy-pages.yml` — 자동 Pages 배포

게임을 수정할 때는 원본 단일 HTML을 다시 gzip+base64로 만들고 payload 조각 및 `EXPECTED_HTML_SHA256`을 갱신하면 됩니다.
