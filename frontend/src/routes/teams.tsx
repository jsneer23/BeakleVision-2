import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router"
import { Box, Heading, Text, Button } from "@chakra-ui/react"
import { Nav } from "@/components/Common/NewNav"

export const Route = createFileRoute("/teams")({
  component: TestPage,
})

// Define the component that will be rendered for this route
function TestPage() {
  return (
    <Box p={8}>
      <Heading mb={4}>Test Page</Heading>
      <Text mb={4}>This is a test page!</Text>
    </Box>
  )
}