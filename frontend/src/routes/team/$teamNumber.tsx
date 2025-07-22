import {
  useParams,
  createFileRoute,
} from "@tanstack/react-router"
import { Box, Heading, Text } from "@chakra-ui/react"
import { Nav } from "@/components/Common/NewNav"

export const Route = createFileRoute("/team/$teamNumber")({
  component: TeamPage,
})

// Define the component that will be rendered for this route
function TeamPage() {
  const { teamNumber } = useParams({ from: '/team/$teamNumber' })
  return (
    <Box p={8}>
      <Nav />
      <Heading mb={4}>Team Page</Heading>
      <Text mb={4}>This is the page for team {teamNumber}!</Text>
    </Box>
  )
}