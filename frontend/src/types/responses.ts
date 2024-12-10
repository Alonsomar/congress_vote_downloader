export interface PaginatedResponse<T> {
  count: number;
  next: boolean;
  previous: boolean;
  results: T[];
}

export interface ApiError {
  message: string;
  status: number;
}
