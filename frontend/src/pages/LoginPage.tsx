import { Button, Card, CardContent, Stack, TextField, Typography } from '@mui/material'
import { useForm } from 'react-hook-form'

type LoginFormValues = {
  email: string
  password: string
}

const LoginPage = () => {
  const { register, handleSubmit, formState } = useForm<LoginFormValues>({
    defaultValues: { email: '', password: '' },
  })

  const onSubmit = handleSubmit(() => {
    // Authentication integration will be added in future iterations.
  })

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Login</Typography>
      <Card>
        <CardContent>
          <Stack component="form" spacing={2} onSubmit={onSubmit}>
            <TextField
              label="Email"
              type="email"
              required
              {...register('email')}
              disabled={formState.isSubmitting}
            />
            <TextField
              label="Password"
              type="password"
              required
              {...register('password')}
              disabled={formState.isSubmitting}
            />
            <Button type="submit" variant="contained">
              Sign In
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  )
}

export default LoginPage
