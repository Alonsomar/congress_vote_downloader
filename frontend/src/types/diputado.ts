export interface Diputado {
    DIPID: string;
    nombre_completo: string;
    sexo: 'M' | 'F';
    fecha_nacimiento?: string;
    region?: string;
    distrito?: string;
    partido?: string;
    comisiones?: string[];
}
  