/*
목적: 정적 데이터 파일을 로드한다.
설명: manifest와 경로 목록을 불러와 배열로 변환한다.
디자인 패턴: 데이터 서비스.
참조: site/data/manifest.json, site/data/docs_paths.txt
*/
import { PathUtils } from "../shared/path-utils.js";

const DATA_BASE = "site/data";

export const DataService = {
  async loadManifest() {
    const response = await fetch(`${DATA_BASE}/manifest.json`);
    if (!response.ok) {
      throw new Error("manifest.json을 불러오지 못했습니다.");
    }
    return response.json();
  },

  async loadPaths(fileName) {
    const response = await fetch(`${DATA_BASE}/${fileName}`);
    if (!response.ok) {
      throw new Error(`${fileName}을 불러오지 못했습니다.`);
    }
    const text = await response.text();
    return text
      .split("\n")
      .map(PathUtils.normalizePath)
      .filter(Boolean);
  },
};
