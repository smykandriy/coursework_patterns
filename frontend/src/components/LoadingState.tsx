import { CircularProgress, Stack, Typography } from '@mui/material'

const LoadingState = ({ label = 'Loading...' }: { label?: string }) => {
  return (
    <Stack direction="row" spacing={2} alignItems="center" justifyContent="center" sx={{ py: 3 }}>
      <CircularProgress size={24} />
      <Typography>{label}</Typography>
    </Stack>
  )
}

export default LoadingState
