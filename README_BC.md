# VR Teleoperation — Final Configuration

## Final Execution Command

2026-09-18 로봇 연구실에서 성공한 최종 실행 명령어.

```bash
python main_vr_scene.py --fov-scale-x 0.5
```

## TODO — 2026-09-21 (Monday)

**Goal:** 최종 성공 실험에 사용한 Python 코드와 GitHub 코드의 일치 여부 확인.

- [ ] 로봇 연구실 워크스테이션에서 성공 당시 사용한 `main_vr_scene.py`의 실제 경로 확인
- [ ] 해당 파일에 `--fov-scale-x` 인자가 구현되어 있는지 확인
- [ ] GitHub의 `code/main_vr_scene.py` 및 `code/vr_teleop/main_vr_scene.py`와 비교
- [ ] 최종 성공 코드의 원본을 보존한 뒤 GitHub에 반영
- [ ] 최종 코드 경로와 실행 명령어를 README 및 SETUP 문서에 통일

**Note:** 현재 GitHub의 `code/main_vr_scene.py`에는 `--fov-scale`만 정의되어 있음. 최종 성공 명령어는 연구실 터미널 기록에서 확인한 것이므로 변경하지 말고, 실제 실행한 코드 버전을 먼저 확인할 것.