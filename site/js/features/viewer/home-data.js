/*
목적: 메인 홈 콘텐츠 데이터를 로드한다.
설명: 정적 JSON을 불러와 홈 화면에 전달한다.
디자인 패턴: 데이터 소스 캐시.
참조: site/data/home.json
*/
let cached = null;

export async function loadHomeData() {
  if (cached) {
    return cached;
  }
  try {
    const response = await fetch("site/data/home.json");
    if (!response.ok) {
      throw new Error("home.json을 불러오지 못했습니다.");
    }
    cached = await response.json();
    return cached;
  } catch (error) {
    cached = null;
    return null;
  }
}
