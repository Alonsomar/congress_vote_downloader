import axios from 'axios';
import { Diputado } from '../types/diputado';
import { Proyecto } from '../types/proyecto';
import { PaginatedResponse } from '../types/responses';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchDiputados = async (page: number = 1, filters?: { nombre?: string; sexo?: string }) => {
  const params = new URLSearchParams({ page: page.toString(), ...filters });
  const { data } = await api.get<PaginatedResponse<Diputado>>(`/diputados/?${params}`);
  return data;
};

export const fetchProyectos = async (page: number = 1) => {
  const { data } = await api.get<PaginatedResponse<Proyecto>>(`/proyectos/?page=${page}`);
  return data;
};

export const searchProyectos = async (searchParams: {
  titulo?: string;
  estado?: string;
  fecha_desde?: string;
  fecha_hasta?: string;
  materias?: string[];
  autores?: string[];
  page?: number;
}) => {
  const { data } = await api.post<PaginatedResponse<Proyecto>>('/proyectos/search/', searchParams);
  return data;
};

export default api;
