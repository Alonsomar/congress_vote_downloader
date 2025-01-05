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

export const fetchDiputados = async (
  page: number = 1, 
  filters?: { 
    nombre?: string; 
    sexo?: string; 
    region?: string; 
    partido?: string 
  }, 
  pageSize: number = 20,
  sortBy: string = 'nombre'
) => {
  const params = new URLSearchParams({ 
    page: page.toString(), 
    page_size: pageSize.toString(),
    sort_by: sortBy,
    ...filters 
  });
  const { data } = await api.get<PaginatedResponse<Diputado>>(`/diputados/?${params}`);
  return data;
};

export const fetchProyectos = async (
  page: number = 1,
  filters?: {
    titulo?: string;
    estado?: string;
    fecha_desde?: string;
    fecha_hasta?: string;
    materias?: string[];
    autores?: string[];
  },
  pageSize: number = 20
) => {
  const params = new URLSearchParams();
  params.append('page', page.toString());
  params.append('page_size', pageSize.toString());
  
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else if (value.trim() !== '') {
          params.append(key, value);
        }
      }
    });
  }

  const { data } = await api.get<PaginatedResponse<Proyecto>>(`/proyectos/?${params}`);
  return data;
};

export const fetchProyectoDetail = async (boletin: string) => {
  const { data } = await api.get<Proyecto>(`/proyectos/${boletin}/`);
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

export const fetchDiputadosStats = async () => {
  const { data } = await api.get<{
    total: number;
    mujeres: number;
    asistenciaPromedio: number;
    proyectosPresentados: number;
  }>('/diputados/stats/');
  return data;
};

interface DiputadosOptions {
  partidos: string[];
  regiones: string[];
  comisiones: string[];
}

export const fetchDiputadosOptions = async () => {
  const { data } = await api.get<DiputadosOptions>('/diputados/options/');
  return data;
};

export default api;
