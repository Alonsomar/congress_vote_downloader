import { Box, Container, Flex } from '@chakra-ui/react';
import { Link } from 'react-router-dom';

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <Box minH="100vh">
      <Flex as="nav" bg="blue.700" color="white" p={4} mb={8}>
        <Container maxW="container.xl">
          <Flex gap={6}>
            <Link to="/diputados" style={{ color: 'white' }}>Diputados</Link>
            <Link to="/proyectos" style={{ color: 'white' }}>Proyectos</Link>
          </Flex>
        </Container>
      </Flex>
      <Container maxW="container.xl">
        {children}
      </Container>
    </Box>
  );
};

export default MainLayout;
