import { 
  Box, 
  Heading, 
  Text, 
  Stack, 
  Badge, 
  HStack, 
  VStack, 
  Icon,
  Tooltip 
} from '@chakra-ui/react';
import { FaMapMarkerAlt, FaBuilding, FaUsers } from 'react-icons/fa';
import { Diputado } from '../../types/diputado';

interface Props {
  diputado: Diputado;
}

const DiputadoCard: React.FC<Props> = ({ diputado }) => {
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
          <Heading size="md" noOfLines={2}>
            {diputado.nombre_completo}
          </Heading>
          <Badge 
            colorScheme={diputado.sexo === 'M' ? 'blue' : 'pink'}
            fontSize="sm"
            px={3}
            py={1}
            borderRadius="full"
          >
            {diputado.sexo === 'M' ? 'Masculino' : 'Femenino'}
          </Badge>
        </HStack>

        <Stack spacing={3} width="100%">
          {diputado.fecha_nacimiento && (
            <Text fontSize="sm" color="gray.600">
              Fecha de nacimiento: {new Date(diputado.fecha_nacimiento).toLocaleDateString()}
            </Text>
          )}

          {diputado.region && (
            <HStack>
              <Icon as={FaMapMarkerAlt} color="gray.500" />
              <Text fontSize="sm">
                Región: {diputado.region}
                {diputado.distrito && ` - Distrito ${diputado.distrito}`}
              </Text>
            </HStack>
          )}

          {diputado.partido && (
            <HStack>
              <Icon as={FaBuilding} color="gray.500" />
              <Text fontSize="sm">
                Partido: {diputado.partido}
              </Text>
            </HStack>
          )}

          {diputado.comisiones && diputado.comisiones.length > 0 && (
            <HStack align="start">
              <Icon as={FaUsers} color="gray.500" mt={1} />
              <VStack align="start" spacing={1}>
                <Text fontSize="sm" fontWeight="medium">Comisiones:</Text>
                {diputado.comisiones.slice(0, 3).map((comision, index) => (
                  <Text key={index} fontSize="sm" color="gray.600" noOfLines={1}>
                    • {comision}
                  </Text>
                ))}
                {diputado.comisiones.length > 3 && (
                  <Tooltip label={diputado.comisiones.slice(3).join('\n')}>
                    <Text fontSize="sm" color="blue.500" cursor="pointer">
                      +{diputado.comisiones.length - 3} más
                    </Text>
                  </Tooltip>
                )}
              </VStack>
            </HStack>
          )}
        </Stack>
      </VStack>
    </Box>
  );
};

export default DiputadoCard;
