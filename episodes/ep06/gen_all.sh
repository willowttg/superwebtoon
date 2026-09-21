#!/usr/bin/env bash
# EP.06 컷 생성. 저장소 루트에서: set -a && . /path/to/.env && set +a && bash episodes/ep06/gen_all.sh [cut...]
S=assets/samples; E=episodes/ep06; R=$E/ref
g(){ n=$1; shift; python scripts/gen_image.py --prompt-file $E/prompts/$n.txt "$@" --out $E/img/$n.png --quality medium || echo "FAIL $n"; }
want(){ [ $# -eq 0 ] && return 0; for w in "$@"; do [ "$w" = "$n" ] && return 0; done; return 1; }
ARGS=("$@")
for n in cover cut1 cut2 cut3 cut4 cut5 cut6 cut7; do
  want "${ARGS[@]}" || continue
  case $n in
    cut2|cut7) g $n --ref $S/tangja-sheet.png --ref $S/dubu-sheet.png --ref $R/lineup-tangja-dubu.png ;;
    cut3)      g $n --ref $S/tangja-sheet.png --ref $S/sora-sheet.png --ref $R/lineup-tangja-sora.png ;;
    *)         g $n --ref $S/tangja-sheet.png ;;
  esac
done
echo ALLDONE
