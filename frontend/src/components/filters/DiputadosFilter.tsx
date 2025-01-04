import { 
  Box, 
  Input, 
  Select, 
  Stack, 
  HStack,
  Button,
  Icon,
  useDisclosure,
  Collapse,
  VStack,
  Text,
  Divider,
  SimpleGrid,
  InputGroup,
  InputLeftElement
} from '@chakra-ui/react';
import { FaFilter, FaSearch, FaTimes } from 'react-icons/fa';
import { useState, useEffect, useCallback } from 'react';
import debounce from 'lodash/debounce';
import { useQuery } from '@tanstack/react-query';
import { fetchDiputadosOptions } from '../../services/api';

interface DiputadosFilterProps {
  onFilterChange: (filters: FilterValues) => void;
  loading?: boolean;
}

interface FilterValues {
  nombre?: string;
  sexo?: string;
  region?: string;
  partido?: string;
  comision?: string;
}

const DiputadosFilter: React.FC<DiputadosFilterProps> = ({ onFilterChange, loading }) => {
  const [localFilters, setLocalFilters] = useState<FilterValues>({});
  const { isOpen, onToggle } = useDisclosure();

  const { data: options } = useQuery({
    queryKey: ['diputados-options'],
    queryFn: fetchDiputadosOptions
  });

  const debouncedFilterChange = useCallback(
    debounce((newFilters: FilterValues) => {
      onFilterChange(newFilters);
    }, 300),
    [onFilterChange]
  );

  const handleFilterChange = (field: keyof FilterValues, value: string) => {
    const newFilters = { ...localFilters, [field]: value };
    if (!value) delete newFilters[field];
    setLocalFilters(newFilters);
    debouncedFilterChange(newFilters);
  };

  const handleClearFilters = () => {
    setLocalFilters({});
    onFilterChange({});
  };

  useEffect(() => {
    return () => {
      debouncedFilterChange.cancel();
    };
  }, [debouncedFilterChange]);

  const activeFiltersCount = Object.keys(localFilters).length;

  return (
    <Box 
      bg="white" 
      p={6} 
      borderRadius="xl" 
      shadow="sm"
      borderWidth="1px"
      mb={6}
    >
      <VStack spacing={4} align="stretch">
        <HStack justify="space-between">
          <InputGroup maxW="400px">
            <InputLeftElement pointerEvents="none">
              <Icon as={FaSearch} color="gray.400" />
            </InputLeftElement>
            <Input
              placeholder="Buscar por nombre..."
              value={localFilters.nombre || ''}
              onChange={(e) => handleFilterChange('nombre', e.target.value)}
              isDisabled={loading}
              bg="white"
            />
          </InputGroup>
          <HStack>
            <Button
              leftIcon={<Icon as={FaFilter} />}
              onClick={onToggle}
              variant="ghost"
              colorScheme={isOpen ? "blue" : "gray"}
              size="md"
              isDisabled={loading}
            >
              Filtros avanzados {activeFiltersCount > 0 && `(${activeFiltersCount})`}
            </Button>
            {activeFiltersCount > 0 && (
              <Button
                leftIcon={<Icon as={FaTimes} />}
                onClick={handleClearFilters}
                variant="ghost"
                size="md"
                colorScheme="red"
                isDisabled={loading}
              >
                Limpiar filtros
              </Button>
            )}
          </HStack>
        </HStack>

        <Collapse in={isOpen}>
          <Box pt={4}>
            <Divider mb={4} />
            <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
              <VStack align="start">
                <Text fontSize="sm" fontWeight="medium" color="gray.700">
                  Género
                </Text>
                <Select
                  placeholder="Todos los géneros"
                  value={localFilters.sexo || ''}
                  onChange={(e) => handleFilterChange('sexo', e.target.value)}
                  isDisabled={loading}
                >
                  <option value="M">Masculino</option>
                  <option value="F">Femenino</option>
                </Select>
              </VStack>

              <VStack align="start">
                <Text fontSize="sm" fontWeight="medium" color="gray.700">
                  Región
                </Text>
                <Select
                  placeholder="Todas las regiones"
                  value={localFilters.region || ''}
                  onChange={(e) => handleFilterChange('region', e.target.value)}
                  isDisabled={loading}
                >
                  {options?.regiones.map((region: string) => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </Select>
              </VStack>

              <VStack align="start">
                <Text fontSize="sm" fontWeight="medium" color="gray.700">
                  Partido Político
                </Text>
                <Select
                  placeholder="Todos los partidos"
                  value={localFilters.partido || ''}
                  onChange={(e) => handleFilterChange('partido', e.target.value)}
                  isDisabled={loading}
                >
                  {options?.partidos.map((partido: string) => (
                    <option key={partido} value={partido}>{partido}</option>
                  ))}
                </Select>
              </VStack>

              <VStack align="start">
                <Text fontSize="sm" fontWeight="medium" color="gray.700">
                  Comisión
                </Text>
                <Select
                  placeholder="Todas las comisiones"
                  value={localFilters.comision || ''}
                  onChange={(e) => handleFilterChange('comision', e.target.value)}
                  isDisabled={loading}
                >
                  {options?.comisiones.map((comision: string) => (
                    <option key={comision} value={comision}>{comision}</option>
                  ))}
                </Select>
              </VStack>
            </SimpleGrid>
          </Box>
        </Collapse>
      </VStack>
    </Box>
  );
};

export default DiputadosFilter;