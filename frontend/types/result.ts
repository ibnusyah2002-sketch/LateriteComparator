export interface QaqcValues {
  ni: number;
  co: number;
  fe: number;
  mgo: number;
  sio2: number;
}

export interface DescriptionAttribute {
  label: string;
  value: string;
}

export interface AlternativeMatch {
  code: string;
  similarity: number;
}

export interface ComparatorResult {
  code: string;
  zone: string;
  color: string;
  similarity: number;
  confidence: string;
  qaqc: QaqcValues;
  descriptionAttributes: DescriptionAttribute[];
  keterangan: string;
  alternativeMatches: AlternativeMatch[];
}
