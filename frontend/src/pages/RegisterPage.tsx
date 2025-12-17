import { Button, Card, CardContent, Stack, TextField, Typography } from '@mui/material'
import { useForm } from 'react-hook-form'

type RegisterFormValues = {
  name: string
  email: string
  password: string
}

const RegisterPage = () => {
  const { register, handleSubmit, formState } = useForm<RegisterFormValues>({
    defaultValues: { name: '', email: '', password: '' },
  })

  const onSubmit = handleSubmit(() => {
    // Registration flow will be added alongside authentication services later.
  })

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Register</Typography>
      <Card>
        <CardContent>
          <Stack component="form" spacing={2} onSubmit={onSubmit}>
            <TextField label="Full Name" required {...register('name')} />
            <TextField label="Email" type="email" required {...register('email')} />
            <TextField
              label="Password"
              type="password"
              required
              {...register('password')}
            />
            <Button type="submit" variant="contained" disabled={formState.isSubmitting}>
              Create Account
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  )
}

export default RegisterPage
