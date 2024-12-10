import { Box, Heading, Text, Stack, Badge } from '@chakra-ui/react';
import { Proyecto } from '../../types/proyecto';

interface Props {
  proyecto: Proyecto;
}

const ProyectoCard: React.FC<Props> = ({ proyecto }) => {
  return (
    <Box
      p={5}
      shadow="md"
      borderWidth="1px"
      borderRadius="lg"
      _hover={{ shadow: 'lg' }}
      transition="all 0.2s"
    >
      <Stack align="start" spacing="3">
        <Heading size="sm">{proyecto.titulo}</Heading>
        <Stack direction="row">
          <Badge colorScheme="blue">Boletín: {proyecto.boletin}</Badge>
          <Badge colorScheme="green">{proyecto.estado}</Badge>
        </Stack>
        <Text fontSize="sm">
          Fecha: {proyecto.fecha_ingreso ? new Date(proyecto.fecha_ingreso).toLocaleDateString() : 'No disponible'}
        </Text>
        {proyecto.autores && proyecto.autores.length > 0 && (
          <Text fontSize="sm">
            Autores: {proyecto.autores.join(', ')}
          </Text>
        )}
      </Stack>
    </Box>
  );
};

export default ProyectoCard;