import { Box, Container, Heading, SimpleGrid, Spinner, Text } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { fetchDiputados } from '../services/api';
import { useState } from 'react';
import DiputadosFilter from '../components/filters/DiputadosFilter';
import DiputadoCard from '../components/cards/DiputadoCard';
import Pagination from '../components/common/Pagination';

const DiputadosPage = () => {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<{ nombre?: string; sexo?: string }>({});

  const { data, isLoading, error } = useQuery({
    queryKey: ['diputados', page, filters],
    queryFn: () => fetchDiputados(page, filters)
  });

  if (isLoading) return (
    <Container centerContent py={10}>
      <Spinner size="xl" />
    </Container>
  );

  if (error) return (
    <Container centerContent py={10}>
      <Text color="red.500">Error al cargar los datos</Text>
    </Container>
  );

  return (
    <Box p={8}>
      <Heading mb={6}>Diputados de Chile</Heading>
      <DiputadosFilter onFilterChange={setFilters} />
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
        {data?.results.map(diputado => (
          <DiputadoCard key={diputado.DIPID} diputado={diputado} />
        ))}
      </SimpleGrid>
      <Pagination
        currentPage={page}
        hasNext={data?.next || false}
        hasPrevious={data?.previous || false}
        onPageChange={setPage}
        totalItems={data?.count || 0}
      />
    </Box>
  );
};

export default DiputadosPage;