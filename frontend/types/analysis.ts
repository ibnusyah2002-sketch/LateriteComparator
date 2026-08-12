export type AnalysisImage = {
    storage_path: string | null;
    local_path: string | null;
    signed_url: string | null;
    signed_url_expires_in: number | null;
  };
  
  export type TopCandidate = {
    code: string | null;
    score: number | null;
    confidence_label: string | null;
    zone: string | null;
    color: string | null;
    description: string | null;
    qaqc: {
      ni: number | null;
      co: number | null;
      fe: number | null;
      sio2: number | null;
      mgo: number | null;
      fe_ni: number | null;
      s_m: number | null;
    };
    local_path: string | null;
    storage_path: string | null;
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
      method: string | null;
      note: string | null;
      top_candidates?: TopCandidate[];
    };
    analysis_request?: {
      source: string | null;
      image_received: boolean;
      image_size_characters: number;
      image_mime_type?: string;
      image_size_bytes?: number;
      image_saved_path?: string;
      matched_code?: string;
      mode?: string;
      preprocessing_method?: string | null;
      preprocessed_image_saved_path?: string | null;
      preprocessing_crop_ratio?: number | null;
      original_image_size?: [number, number] | null;
      processed_image_size?: [number, number] | null;
    };
  };