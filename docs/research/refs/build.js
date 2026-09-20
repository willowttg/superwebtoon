// docs/research/refs/index.html 생성기. 계정 폴더의 캡처(profile.jpg, postN-sM.jpg)를 훑어 갤러리를 만든다.
// 실행: node docs/research/refs/build.js
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const ACCOUNTS = [
  ['sombi.ya', '솜비 | HSP + 심리툰', '1.7만', '예민한 사람·HSP 특징을 캐릭터로 풀어낸 심리툰. "둥글어 보이지만 사실은 예민한 사람들 특징" 같은 정체성 호명형 표지 → 특징 나열 → 위로. 우리 콘셉트와 구조가 가장 가깝다. 좋아요 대비 공유·저장 비율이 높음.'],
  ['seobam_breeze', '서늘한여름밤 | 심리학자', '7만', '심리학자의 그림일기. 표지가 곧 위로 문장("너는 외롭게 있기에는 아까운 사람!"), 흰 배경에 최소 선 캐릭터. 반전 이후 5컷 "위로 한 줄"의 톤 레퍼런스.'],
  ['yangchikii', '약치기그림 · 그림왕양치기', '13.3만', '직장인 상황을 정밀하게 묘사한 뒤 캘리그라피 대사로 카타르시스. 1~2컷 공감 최고조 파트의 레퍼런스. 사실적 인체 + 담백한 배경.'],
  ['harusal_22', '하루살이 | 직장인툰', '7.3만', '"나만 못 버티나 싶을 때" — 정체성 호명 후킹 표지의 정석. 굵은 제목 텍스트 + 3등신 햄스터 캐릭터. 회사툰 시즌제지만 각 편은 단독으로 읽힘.'],
  ['keykney', '키크니', '123.5만', '팔로워 사연을 그려주는 사연툰. 손글씨 + 흰 배경 + 단순 선. 텍스트가 그림보다 큰 비중. 소통 자체가 콘텐츠가 되는 구조.'],
  ['punj_toon', '펀자이씨툰', '20.1만', '연필 드로잉 + 손글씨. 치매 할머니와 가족의 일상을 편마다 완결되는 단편으로. 잔잔한 위로 톤, 게시물당 좋아요 1~2만.'],
  ['gimgre', '김그래 <그래일기>', '10.4만', '그림일기형 에세이툰. 저채도 수채 + 문장력("시절인연"). 세로 2컷 구성. 위로 마무리 문장 참고.'],
  ['drawing_baepsae', '뱁새', '13.7만', '개그 일상 단편. 표지 = 대형 검정 텍스트 + 포인트 컬러(핑크) 헤드라인 + 캐릭터 클로즈업. 표지 레이아웃 참고.'],
  ['i_iary2', '이아리', '13.6만', '연애·일상 단편. 파스텔 단색 배경, 깔끔한 선, 3등신 캐릭터. 게시물당 좋아요 1.2만+. 피드 톤 통일의 좋은 예.'],
  ['woodpencil02', '이연필', '10.9만', 'MBTI F/T 성향 소재의 일상툰(F 생존기). 성격 유형을 소재로 삼아 "완전 나야" 태그를 유발하는 구조 참고.'],
  ['runotoon', '르노', '9.2만', '개그 일상 단편. "~했는데 ~한 만화" 제목 공식 + 표지에 상황 요약 텍스트 박스. 컷 안 텍스트 배치 참고.'],
  ['mbti_toon', 'MBTI 관계성 보고서', '4.2만', '16유형 캐릭터로 에피소드 구성. 유형별 시리즈 해시태그로 세계관 축적 → 정체성 태그 바이럴.'],
  ['bonein.manhwa', '김지민', '6.7만', '낙서 수준 선화 + B급 개그로 한 달 만에 급성장. "작화 퀄리티보다 자연스러움" 의 증거 사례.'],
];

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

const sections = ACCOUNTS.map(([h, name, fol, note]) => {
  const dir = path.join(ROOT, h);
  if (!fs.existsSync(dir)) return '';
  const files = fs.readdirSync(dir).filter(f => /^post\d+-s\d+\.jpg$/.test(f));
  const posts = {};
  for (const f of files) {
    const [, p, s] = f.match(/^post(\d+)-s(\d+)\.jpg$/);
    (posts[p] ||= []).push([+s, f]);
  }
  const strips = Object.keys(posts).sort((a, b) => a - b).map(p => {
    const imgs = posts[p].sort((a, b) => a[0] - b[0])
      .map(([, f]) => `<img loading="lazy" src="${h}/${f}" alt="">`).join('');
    return `<div class="strip">${imgs}</div>`;
  }).join('\n');
  return `
<section id="${h}">
  <h2><a href="https://www.instagram.com/${h}/" target="_blank" rel="noopener">@${h}</a> <small>${esc(name)} · 팔로워 ${fol}</small></h2>
  <p>${esc(note)}</p>
  <details><summary>프로필 피드</summary><img loading="lazy" class="profile" src="${h}/profile.jpg" alt=""></details>
  ${strips}
</section>`;
}).join('\n');

const toc = ACCOUNTS.map(([h, name, fol]) => `<a href="#${h}">@${h}</a>`).join(' · ');

const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>인스타 일상툰 레퍼런스 캡처</title>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet">
<style>
  :root{--ink:#3A3733;--point:#C77B3F}
  *{box-sizing:border-box}
  body{margin:0;padding:40px 16px 96px;background:#EFEAE2;color:var(--ink);font-family:'Gowun Dodum','Malgun Gothic',sans-serif;line-height:1.6}
  main{max-width:960px;margin:0 auto}
  h1{font-size:22px;margin:0 0 6px}
  .sub{font-size:13px;color:#8A837A;margin:0 0 8px}
  .toc{font-size:13px;margin:0 0 32px;line-height:2}
  a{color:var(--point)}
  section{background:#FFFDF9;border-radius:12px;padding:16px 16px 8px;margin-bottom:20px;box-shadow:0 2px 14px rgba(58,55,51,.08)}
  h2{font-size:17px;margin:0 0 4px;font-weight:400}
  h2 small{font-size:12px;color:#8A837A;margin-left:6px}
  section p{font-size:14px;margin:0 0 12px}
  details{margin-bottom:12px;font-size:13px;color:#8A837A}
  details summary{cursor:pointer}
  img.profile{display:block;width:100%;max-width:640px;margin-top:8px;border-radius:8px}
  .strip{display:flex;gap:6px;overflow-x:auto;padding:4px 0 12px;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory}
  .strip img{height:300px;flex:none;border-radius:6px;background:#eee;scroll-snap-align:start}
  @media(min-width:700px){.strip img{height:380px}}
  .foot{font-size:12px;color:#8A837A;margin-top:32px}
</style>
</head>
<body>
<main>
  <h1>인스타 일상툰 레퍼런스 캡처</h1>
  <p class="sub">2026-09-20 채집 · 편마다 완결되는 일상·공감·심리툰 위주 · 콘셉트 근접도 순. 각 게시물은 좌우 스크롤로 슬라이드 확인.</p>
  <p class="toc">${toc}</p>
${sections}
  <p class="foot">모든 이미지의 저작권은 각 작가에게 있으며 내부 참고 목적으로만 캡처했다. 분석 메모: <a href="https://github.com/willowttg/superwebtoon/blob/master/docs/research/03-instatoon-references.md">03-instatoon-references.md</a></p>
</main>
</body>
</html>
`;
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('wrote index.html,', ACCOUNTS.length, 'accounts');
