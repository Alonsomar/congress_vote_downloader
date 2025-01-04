import { Badge, Box, HStack, Text } from "@chakra-ui/react";
import { Diputado } from "../../types/diputado";

const DiputadoListItem: React.FC<{ diputado: Diputado }> = ({ diputado }) => {
  return (
    <Box
      w="100%"
      p={4}
      borderWidth="1px"
      borderRadius="lg"
      display="flex"
      justifyContent="space-between"
      alignItems="center"
    >
      <HStack spacing={4}>
        <Text fontWeight="bold">{diputado.nombre_completo}</Text>
        <Badge colorScheme={diputado.partido ? 'blue' : 'gray'}>
          {diputado.partido || 'Independiente'}
        </Badge>
      </HStack>
      <Text color="gray.600">{diputado.region}</Text>
    </Box>
  );
};

export default DiputadoListItem;
