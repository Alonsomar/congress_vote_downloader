import { 
  Box,
  Input,
  Select,
  FormControl,
  FormLabel,
  VStack,
  HStack
} from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import debounce from 'lodash/debounce';

interface ProyectosFilterProps {
  onFilterChange: (filters: {
    titulo?: string;
    estado?: string;
    fecha_desde?: string;
    fecha_hasta?: string;
    materias?: string[];
    autores?: string[];
  }) => void;
}

const ProyectosFilter = ({ onFilterChange }: ProyectosFilterProps) => {
  const [localFilters, setLocalFilters] = useState({
    titulo: '',
    estado: '',
    fecha_desde: '',
    fecha_hasta: '',
  });

  // Debounced filter change handler
  const debouncedFilterChange = debounce((newFilters) => {
    onFilterChange(newFilters);
  }, 500);

  useEffect(() => {
    return () => {
      debouncedFilterChange.cancel();
    };
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const newFilters = { ...localFilters, [name]: value };
    setLocalFilters(newFilters);
    
    if (name === 'titulo') {
      debouncedFilterChange(newFilters);
    } else {
      onFilterChange(newFilters);
    }
  };

  return (
    <Box p={4} bg="white" borderRadius="md" shadow="sm">
      <VStack spacing={4}>
        <FormControl>
          <FormLabel>Título</FormLabel>
          <Input
            name="titulo"
            value={localFilters.titulo}
            onChange={handleChange}
            placeholder="Buscar por título..."
          />
        </FormControl>

        <FormControl>
          <FormLabel>Estado</FormLabel>
          <Select
            name="estado"
            value={localFilters.estado}
            onChange={handleChange}
            placeholder="Seleccionar estado"
          >
            <option value="Publicado">Publicado</option>
            <option value="En tramitación">En tramitación</option>
            <option value="Archivado">Archivado</option>
          </Select>
        </FormControl>

        <HStack spacing={4} width="100%">
          <FormControl>
            <FormLabel>Fecha desde</FormLabel>
            <Input
              name="fecha_desde"
              type="date"
              value={localFilters.fecha_desde}
              onChange={handleChange}
            />
          </FormControl>

          <FormControl>
            <FormLabel>Fecha hasta</FormLabel>
            <Input
              name="fecha_hasta"
              type="date"
              value={localFilters.fecha_hasta}
              onChange={handleChange}
            />
          </FormControl>
        </HStack>
      </VStack>
    </Box>
  );
};

export default ProyectosFilter;
