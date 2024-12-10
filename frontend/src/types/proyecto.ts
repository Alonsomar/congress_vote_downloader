export interface Proyecto {
    boletin: string;
    titulo?: string;
    estado?: string;
    etapa?: string;
    subetapa?: string;
    urgencia_actual?: string;
    fecha_ingreso?: string | null;
    autores?: string[];
    // añade más campos según tu schema final
  }
  