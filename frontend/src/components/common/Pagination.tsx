import { 
  HStack, 
  Button, 
  Text, 
  Select,
  useBreakpointValue
} from '@chakra-ui/react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  totalItems?: number;
  pageSize?: number;
  onPageSizeChange?: (pageSize: number) => void;
  isLoading?: boolean;
}

const Pagination = ({ 
  currentPage, 
  totalPages, 
  onPageChange,
  totalItems,
  pageSize,
  onPageSizeChange,
  isLoading 
}: PaginationProps) => {
  const isMobile = useBreakpointValue({ base: true, md: false });

  const renderPageNumbers = () => {
    const pages = [];
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    if (startPage > 1) {
      pages.push(1);
      if (startPage > 2) pages.push('...');
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) pages.push('...');
      pages.push(totalPages);
    }

    return pages.map((page, index) => {
      if (page === '...') {
        return <Text key={`ellipsis-${index}`}>...</Text>;
      }
      return (
        <Button
          key={page}
          onClick={() => onPageChange(Number(page))}
          colorScheme={currentPage === page ? 'blue' : 'gray'}
          variant={currentPage === page ? 'solid' : 'ghost'}
          size="sm"
        >
          {page}
        </Button>
      );
    });
  };

  return (
    <HStack spacing={4} justify="center" my={6}>
      {!isMobile && totalItems && (
        <Text fontSize="sm" color="gray.600">
          Total: {totalItems} resultados
        </Text>
      )}

      <Button
        leftIcon={<FaChevronLeft />}
        onClick={() => onPageChange(currentPage - 1)}
        isDisabled={currentPage === 1 || isLoading}
        size="sm"
        variant="ghost"
      >
        {isMobile ? '' : 'Anterior'}
      </Button>

      {!isMobile && renderPageNumbers()}

      <Button
        rightIcon={<FaChevronRight />}
        onClick={() => onPageChange(currentPage + 1)}
        isDisabled={currentPage === totalPages || isLoading}
        size="sm"
        variant="ghost"
      >
        {isMobile ? '' : 'Siguiente'}
      </Button>

      {onPageSizeChange && (
        <HStack spacing={2}>
          <Text fontSize="sm">Mostrar:</Text>
          <Select
            size="sm"
            width="auto"
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </Select>
        </HStack>
      )}
    </HStack>
  );
};

export default Pagination;
