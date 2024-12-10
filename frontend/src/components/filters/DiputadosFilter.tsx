import { Box, Input, Select as ChakraSelect, Stack } from '@chakra-ui/react';
import { ChangeEvent } from 'react';

interface DiputadosFilterProps {
  onFilterChange: (filters: { nombre?: string; sexo?: string }) => void;
}

const DiputadosFilter = ({ onFilterChange }: DiputadosFilterProps) => {
  return (
    <Box mb={6}>
      <Stack direction="row" gap="24px">
        <Input
          placeholder="Buscar por nombre..."
          onChange={(e: ChangeEvent<HTMLInputElement>) => 
            onFilterChange({ nombre: e.target.value })}
        />
        <ChakraSelect
          placeholder="Filtrar por sexo"
          onChange={(e: ChangeEvent<HTMLSelectElement>) => 
            onFilterChange({ sexo: e.target.value })}
        >
          <option value="M">Masculino</option>
          <option value="F">Femenino</option>
        </ChakraSelect>
      </Stack>
    </Box>
  );
};

export default DiputadosFilter;