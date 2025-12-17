import { Alert } from '@mui/material'

const ErrorAlert = ({ message }: { message?: string }) => {
  if (!message) return null
  return (
    <Alert severity="error" sx={{ mb: 2 }}>
      {message}
    </Alert>
  )
}

export default ErrorAlert
