export interface Proyecto {
  boletin: string;
  titulo?: string;
  estado?: string;
  etapa?: string;
  subetapa?: string;
  urgencia_actual?: string;
  fecha_ingreso?: string;
  iniciativa?: string;
  camara_origen?: string;
  link_mensaje_mocion?: string;
  ley?: {
    numero?: string;
    fecha_publicacion?: string;
  };
  refundidos?: string[];
  autores?: string[];
  materias?: string[];
  tramitacion?: {
    sesion?: string;
    fecha?: string;
    descripcion?: string;
    etapa?: string;
    camara?: string;
  }[];
  votaciones?: any[];
  urgencias?: any[];
  informes?: any[];
  oficios?: any[];
  indicaciones?: any[];
}
  