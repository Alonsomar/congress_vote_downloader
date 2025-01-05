import { 
  Box, 
  Heading, 
  Text, 
  Stack, 
  Badge, 
  VStack, 
  HStack,
  Icon,
  Tooltip,
  Link
} from '@chakra-ui/react';
import { FaCalendar, FaUser, FaTag, FaExternalLinkAlt } from 'react-icons/fa';
import { Proyecto } from '../../types/proyecto';

interface Props {
  proyecto: Proyecto;
}

const ProyectoCard: React.FC<Props> = ({ proyecto }) => {
  return (
    <Box
      p={6}
      shadow="lg"
      borderWidth="1px"
      borderRadius="xl"
      bg="white"
      _hover={{ 
        transform: 'translateY(-2px)',
        shadow: '2xl'
      }}
      transition="all 0.2s"
    >
      <VStack align="start" spacing={4}>
        <HStack justify="space-between" width="100%">
          <Badge colorScheme="blue">Boletín: {proyecto.boletin}</Badge>
          <Badge 
            colorScheme={
              proyecto.estado === 'Publicado' ? 'green' : 
              proyecto.estado === 'En tramitación' ? 'yellow' : 
              'gray'
            }
          >
            {proyecto.estado}
          </Badge>
        </HStack>

        <Heading size="md" noOfLines={2}>
          {proyecto.titulo}
        </Heading>

        <Stack spacing={3} width="100%">
          <HStack>
            <Icon as={FaCalendar} color="gray.500" />
            <Text fontSize="sm">
              Ingreso: {proyecto.fecha_ingreso ? 
                new Date(proyecto.fecha_ingreso).toLocaleDateString() : 
                'No disponible'}
            </Text>
          </HStack>

          {proyecto.autores && proyecto.autores.length > 0 && (
            <HStack align="start">
              <Icon as={FaUser} color="gray.500" mt={1} />
              <VStack align="start" spacing={0}>
                <Text fontSize="sm" fontWeight="medium">Autores:</Text>
                <Text fontSize="sm" noOfLines={2}>
                  {proyecto.autores.join(', ')}
                </Text>
              </VStack>
            </HStack>
          )}

          {proyecto.materias && proyecto.materias.length > 0 && (
            <HStack align="start">
              <Icon as={FaTag} color="gray.500" mt={1} />
              <VStack align="start" spacing={0}>
                <Text fontSize="sm" fontWeight="medium">Materias:</Text>
                <Text fontSize="sm" noOfLines={2}>
                  {proyecto.materias.join(', ')}
                </Text>
              </VStack>
            </HStack>
          )}

          {proyecto.link_mensaje_mocion && (
            <Link 
              href={proyecto.link_mensaje_mocion} 
              isExternal
              color="blue.500"
              fontSize="sm"
              display="flex"
              alignItems="center"
            >
              Ver documento original
              <Icon as={FaExternalLinkAlt} ml={2} />
            </Link>
          )}
        </Stack>
      </VStack>
    </Box>
  );
};

export default ProyectoCard;