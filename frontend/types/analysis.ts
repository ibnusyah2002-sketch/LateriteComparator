export type AnalysisImage = {
    storage_path: string | null;
    local_path: string | null;
    signed_url: string | null;
    signed_url_expires_in: number | null;
  };
  
  export type AnalysisPayload = {
    match_type: string;
    message: string;
    matched_sample: {
      id: string | null;
      code: string | null;
      zone: string | null;
      color: string | null;
      size_text: string | null;
      composition: string | null;
      description: string | null;
    };
    qaqc: {
      ni: number | null;
      co: number | null;
      fe: number | null;
      sio2: number | null;
      cao: number | null;
      mgo: number | null;
      fe_ni: number | null;
      s_m: number | null;
    };
    images: {
      raw: AnalysisImage;
      scale: AnalysisImage;
    };
    similarity: {
      score: number | null;
      confidence_label: string | null;
      note: string | null;
    };
  };