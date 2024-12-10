import { Box, Heading, Text, Stack, Badge } from '@chakra-ui/react';
import { Diputado } from '../../types/diputado';

interface Props {
  diputado: Diputado;
}

const DiputadoCard: React.FC<Props> = ({ diputado }) => {
  return (
    <Box
      p={5}
      shadow="md"
      borderWidth="1px"
      borderRadius="lg"
      width="300px"
      m={2}
      _hover={{ shadow: 'lg' }}
      transition="all 0.2s"
    >
      <Stack align="start" spacing="2">
        <Heading size="md">{diputado.nombre_completo}</Heading>
        <Badge colorScheme={diputado.sexo === 'M' ? 'blue' : 'pink'}>
          {diputado.sexo === 'M' ? 'Masculino' : 'Femenino'}
        </Badge>
        <Text fontSize="sm" color="gray.600">
          Nacimiento: {diputado.fecha_nacimiento || 'No especificado'}
        </Text>
      </Stack>
    </Box>
  );
};

export default DiputadoCard;
