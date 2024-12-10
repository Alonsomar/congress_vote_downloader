import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  colors: {
    brand: {
      50: '#f7fafc',
      500: '#718096',
      700: '#2c5282',
      900: '#171923',
    },
  },
  components: {
    Stack: {
      defaultProps: {
        spacing: 4,
      },
    },
    SimpleGrid: {
      defaultProps: {
        spacing: 4,
      },
    },
  },
})

export default theme 