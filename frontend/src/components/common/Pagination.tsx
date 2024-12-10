import { Button, Stack, Text } from '@chakra-ui/react';

interface PaginationProps {
  currentPage: number;
  hasNext: boolean;
  hasPrevious: boolean;
  onPageChange: (page: number) => void;
  totalItems: number;
}

const Pagination = ({ currentPage, hasNext, hasPrevious, onPageChange, totalItems }: PaginationProps) => {
  return (
    <Stack direction="row" gap="24px" justify="center" my={6}>
      <Button 
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!hasPrevious}
      >
        Anterior
      </Button>
      <Text>Página {currentPage}</Text>
      <Button 
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!hasNext}
      >
        Siguiente
      </Button>
      <Text fontSize="sm" color="gray.600">
        Total: {totalItems} items
      </Text>
    </Stack>
  );
};

export default Pagination;
