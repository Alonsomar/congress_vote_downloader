import { useState, useEffect } from 'react';
import api from '../services/api';
import { Diputado } from '../types/diputado';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

function useFetchDiputados(page = 1) {
  const [data, setData] = useState<PaginatedResponse<Diputado> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    api.get(`/diputados/?page=${page}`)
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [page]);

  return { data, loading, error };
}

export default useFetchDiputados;
