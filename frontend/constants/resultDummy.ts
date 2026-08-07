import type { ComparatorResult } from "@/types/result";

/** UI-only dummy comparator result for Sprint 03. Replace with API response later. */
export const RESULT_DUMMY: ComparatorResult = {
  code: "RB4-015",
  zone: "Earthy Saprolite",
  color: "Brown Greenish",
  similarity: 98.7,
  confidence: "Very High",
  qaqc: {
    ni: 1.82,
    co: 0.08,
    fe: 23.41,
    mgo: 9.62,
    sio2: 41.2,
  },
  descriptionAttributes: [
    { label: "Zona", value: "Earthy Saprolite" },
    { label: "Warna", value: "Brown Greenish" },
    { label: "Ukuran", value: "Gravel - Boulder" },
    {
      label: "Komposisi",
      value: "Serpentine, Goethite, Garnierite traces",
    },
    {
      label: "Keterangan",
      value:
        "Weathered ultramafic material with greenish brown tone and earthy texture.",
    },
  ],
  keterangan:
    "Weathered ultramafic material with greenish brown tone and earthy texture.",
  alternativeMatches: [
    { code: "RB4-011", similarity: 95.4 },
    { code: "RB4-007", similarity: 93.8 },
    { code: "RB4-021", similarity: 91.2 },
  ],
};
