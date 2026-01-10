import type { BFI2Questions, BFI2Response, User } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api";

type RequestOptions = {
  method?: string;
  body?: unknown;
};

async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    const message = detail?.detail ?? "Request failed";
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function registerUser(participantId: string, passcode: string): Promise<User> {
  return apiRequest<User>("/auth/register", {
    method: "POST",
    body: { participant_id: participantId, passcode },
  });
}

export function loginUser(participantId: string, passcode: string): Promise<User> {
  return apiRequest<User>("/auth/login", {
    method: "POST",
    body: { participant_id: participantId, passcode },
  });
}

export function updateUser(
  userId: number,
  updates: {
    alias?: string;
    age?: number;
    education?: string;
    gender?: string;
    consented?: boolean;
  }
): Promise<User> {
  return apiRequest<User>(`/users/${userId}`, {
    method: "PATCH",
    body: updates,
  });
}

export function getQuestions(): Promise<BFI2Questions> {
  return apiRequest<BFI2Questions>("/bfi2/questions");
}

export function submitResponses(
  userId: number,
  responses: Record<number, number>,
  surveyType: string
): Promise<BFI2Response> {
  return apiRequest<BFI2Response>("/bfi2/responses", {
    method: "POST",
    body: {
      user_id: userId,
      survey_type: surveyType,
      responses,
    },
  });
}
