export type User = {
  id: number;
  participant_id: string;
  alias?: string | null;
  age?: number | null;
  education?: string | null;
  gender?: string | null;
  consent_signed_at?: string | null;
  created_at: string;
  updated_at: string;
};

export type BFI2Question = {
  id: number;
  text: string;
  domain: string;
  facet: string;
  reverse: boolean;
};

export type BFI2Questions = {
  title: string;
  description: string;
  instructions: string;
  scale: Record<string, string>;
  items: BFI2Question[];
};

export type BFI2Response = {
  id: number;
  user_id: number;
  survey_type: string;
  responses: Record<number, number>;
  scored: {
    summary: Record<string, number>;
    domains: Record<
      string,
      {
        name: string;
        code: string;
        score: number;
        interpretation: string;
      }
    >;
  };
  created_at: string;
  updated_at: string;
};
