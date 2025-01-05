import { 
    Box, 
    Container, 
    Heading, 
    SimpleGrid, 
    Spinner, 
    Text,
    VStack,
    HStack
  } from '@chakra-ui/react';
  import { useQuery } from '@tanstack/react-query';
  import { useState } from 'react';
  import { fetchProyectos } from '../services/api';
  import ProyectoCard from '../components/cards/ProyectoCard';
  import Pagination from '../components/common/Pagination';
  import ProyectosFilter from '../components/filters/ProyectosFilter';
  import { Helmet } from 'react-helmet-async';
  
  const ProyectosPage = () => {
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(20);
    const [filters, setFilters] = useState<{
      titulo?: string;
      estado?: string;
      fecha_desde?: string;
      fecha_hasta?: string;
      materias?: string[];
      autores?: string[];
    }>({});
  
    const { data, isLoading, error } = useQuery({
      queryKey: ['proyectos', page, pageSize, filters],
      queryFn: () => fetchProyectos(page, filters, pageSize),
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
      <>
        <Helmet>
          <title>Proyectos de Ley - Análisis Político</title>
          <meta name="description" content="Listado de proyectos de ley en el Congreso de Chile" />
        </Helmet>
  
        <Box p={8}>
          <Heading mb={6}>Proyectos de Ley</Heading>
          
          <ProyectosFilter onFilterChange={setFilters} />
  
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mt={6}>
            {data?.results?.map(proyecto => (
              <ProyectoCard key={proyecto.boletin} proyecto={proyecto} />
            )) || []}
          </SimpleGrid>
  
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((data?.count || 0) / pageSize)}
            onPageChange={setPage}
            totalItems={data?.count || 0}
            pageSize={pageSize}
            onPageSizeChange={setPageSize}
            isLoading={isLoading}
          />
        </Box>
      </>
    );
  };
  
  export default ProyectosPage;