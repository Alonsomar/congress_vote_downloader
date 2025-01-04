import { Box, Container, Heading, SimpleGrid, Spinner, Text, ButtonGroup, IconButton, Stat, StatNumber, StatLabel, Select, VStack, HStack } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { fetchDiputados, fetchDiputadosStats } from '../services/api';
import { useState } from 'react';
import DiputadosFilter from '../components/filters/DiputadosFilter';
import DiputadoCard from '../components/cards/DiputadoCard';
import Pagination from '../components/common/Pagination';
import { Helmet } from 'react-helmet-async';
import { FaThLarge, FaList } from 'react-icons/fa';
import DiputadoListItem from '../components/items/DiputadoListItem';

interface DiputadosStats {
  total: number;
  mujeres: number;
  asistenciaPromedio: number;
  proyectosPresentados: number;
}

const StatsOverview: React.FC<{ stats: DiputadosStats }> = ({ stats }) => (
  <SimpleGrid columns={{ base: 2, md: 4 }} gap={4} mb={6}>
    <Stat>
      <StatLabel>Total Diputados</StatLabel>
      <StatNumber>{stats.total}</StatNumber>
    </Stat>
    <Stat>
      <StatLabel>Mujeres</StatLabel>
      <StatNumber>{stats.mujeres}</StatNumber>
    </Stat>
    <Stat>
      <StatLabel>Asistencia Promedio</StatLabel>
      <StatNumber>{stats.asistenciaPromedio}%</StatNumber>
    </Stat>
    <Stat>
      <StatLabel>Proyectos Presentados</StatLabel>
      <StatNumber>{stats.proyectosPresentados}</StatNumber>
    </Stat>
  </SimpleGrid>
);

const ViewToggle: React.FC<{ viewMode: 'grid' | 'list'; setViewMode: (mode: 'grid' | 'list') => void }> = ({ viewMode, setViewMode }) => (
  <ButtonGroup size="sm" mb={4}>
    <IconButton
      aria-label="Vista grilla"
      icon={<FaThLarge />}
      isActive={viewMode === 'grid'}
      onClick={() => setViewMode('grid')}
    />
    <IconButton
      aria-label="Vista lista"
      icon={<FaList />}
      isActive={viewMode === 'list'}
      onClick={() => setViewMode('list')}
    />
  </ButtonGroup>
);

const DiputadosPage = () => {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [filters, setFilters] = useState<{ nombre?: string; sexo?: string; region?: string; partido?: string }>({});
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState('nombre');
  const [stats, setStats] = useState<DiputadosStats | null>(null);

  const { data: statsData, isError: isStatsError } = useQuery({
    queryKey: ['diputados-stats'],
    queryFn: fetchDiputadosStats,
    retry: false
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['diputados', page, pageSize, filters, sortBy],
    queryFn: () => fetchDiputados(page, filters, pageSize, sortBy),
    placeholderData: (previousData) => previousData
  });

  const renderDiputados = () => {
    if (!data?.results) return null;
    
    return viewMode === 'grid' ? (
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
        {data.results.map(diputado => (
          <DiputadoCard key={diputado.DIPID} diputado={diputado} />
        ))}
      </SimpleGrid>
    ) : (
      <VStack spacing={4} width="100%">
        {data.results.map(diputado => (
          <DiputadoListItem key={diputado.DIPID} diputado={diputado} />
        ))}
      </VStack>
    );
  };

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

  const totalPages = Math.ceil((data?.count || 0) / pageSize);

  return (
    <>
      <Helmet>
        <title>Diputados de Chile - Análisis Político</title>
        <meta name="description" content="Listado de diputados activos de Chile, con información detallada sobre su trabajo parlamentario." />
      </Helmet>
      
      <Box p={8}>
        <Heading mb={6}>Diputados de Chile</Heading>
        
        {!isStatsError && statsData && <StatsOverview stats={statsData} />}
        
        <HStack justify="space-between" mb={6}>
          <DiputadosFilter onFilterChange={setFilters} loading={isLoading} />
          <HStack spacing={4}>
            <ViewToggle viewMode={viewMode} setViewMode={setViewMode} />
            <Select
              size="sm"
              width="auto"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="nombre">Nombre A-Z</option>
              <option value="partido">Partido</option>
              <option value="region">Región</option>
              <option value="asistencia">Asistencia</option>
            </Select>
          </HStack>
        </HStack>
        
        {renderDiputados()}

        <Pagination
          currentPage={page}
          totalPages={totalPages}
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

export default DiputadosPage;